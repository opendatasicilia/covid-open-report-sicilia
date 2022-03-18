import io
import fitz
import pandas as pd
from PIL import Image
import pytesseract

path = '.'
comuni = pd.DataFrame(pd.read_csv(
    'https://raw.githubusercontent.com/gabacode/vaxExtract/main/utilities/Elenco-comuni-siciliani.csv', converters={'pro_com_t': '{:0>6}'.format}))
latest = pd.DataFrame(pd.read_csv(path+'/download/report.csv')).iloc[-1]
file = latest['nome_file']
date = latest['data_report']


def getPages(file):
    pages = []
    pdf = fitz.open(file)
    print('Determino pagine da leggere...')
    for index in range(len(pdf)):
        page = pdf.load_page(index)
        text = page.get_text()
        if "ALLEGATO" in text:
            pages.append(index)
    output = {
        "data": date,
        "incidenza": list(range(pages[0], pages[1]+1)),
        "vaccini": list(range(pages[1]+1, len(pdf)+1))
    }
    print(output)
    return output


def isDigit(x):
    '''
    True se x contiene un numero
    '''
    try:
        float(x)
        return True
    except ValueError:
        return False


def getIncidenza(file, pages):
    print('Leggo tabella Incidenza...attendi...')
    pdf = fitz.open(file)
    allText = []
    for index in range(pages[0], pages[-1]):
        page = pdf.load_page(index)
        text = page.get_text()
        text = text.replace('\n', ' ')
        allText.append(text[2::])

    # Seleziona parti di interesse, formatta elementi ambigui e ritorna una lista
    out = ' '.join(allText)\
        .rpartition('settimane')[2]\
        .rpartition('Totale')[0]\
        .replace('- ', '-')\
        .replace(',', '.')\
        .replace('---', '0%')\
        .replace('#DIV/0!', '0%')\
        .replace('  ', ' ')\
        .replace('  ', ' ')\
        .replace('  ', ' ')\
        .replace('%', '')\
        .replace("O'", "Ò").replace("I'", "Ì").replace("U'", "Ù")\
        .split()

    # Riconosce il nome del comune rispetto ad un numero e ritorna una nuova lista
    new = ""
    for split in out:
        if not isDigit(split):
            new = new + split + ' '
        if isDigit(split):
            new = new + ',' + split + ','
    new = new.replace(',,', ',').replace(
        ' ,', ',').replace(' -', '-').split(',')

    # Looppa la lista e crea tuple a gruppi di 4
    it = iter(new)
    data = list(zip(it, it, it, it))

    # Crea dataframe
    df = pd.DataFrame(
        data, columns=['comune', 'casi', 'incidenza', 'variazione'])
    df = df[['comune', 'incidenza', 'casi']]

    # Rimuovi distretti (duplicati)
    incidenza = df[~df["comune"].duplicated(keep="last")]
    incidenza.reset_index(inplace=True, drop=True)

    # Inner join e recupera info comuni
    out = pd.merge(incidenza, comuni, left_on=incidenza["comune"].str.lower(
    ), right_on=comuni["comune"].str.lower(), how="inner")
    out.rename(columns={'comune_y': 'comune'}, inplace=True)
    out = out[['cod_prov', 'pro_com_t', 'provincia', 'comune',
               'incidenza', 'casi']].sort_values(by=['provincia', 'comune'])
    out.reset_index(drop=True, inplace=True)
    out.insert(0, 'data', date)

    # Controlla che ci siano tutti i comuni
    assert (len(out) == 390), "Errore: Sono presenti meno comuni del previsto."

    # Esporta CSV
    lastUpdate = open(
        './dati/incidenza/incidenza.csv').read().rsplit('\n', 2)[1].split(',')[0]
    if date != lastUpdate:
        print('Esporto CSV...')
        out.to_csv('./dati/incidenza/incidenza-' +
                   date.replace("-", "")+'.csv', index=None, header=True)
        out.to_csv(path+'/dati/incidenza/incidenza-latest.csv',
                   index=None, header=True)
        out.to_csv(path+'/dati/incidenza/incidenza.csv',
                   mode='a', index=None, header=False)
    csv = path+'/dati/incidenza/incidenza-'+date.replace("-", "")+'.csv'

    return csv


def getVax(file, pages):
    print('Leggo tabella Vaccini...attendi...')
    pdf = fitz.open(file)
    config = r'--oem 3 --psm 6'
    zoom = 3
    mat = fitz.Matrix(zoom, zoom)
    textes = []
    for index in range(pages[0], pages[-1]):
        page = pdf.load_page(index)
        pixmap = page.get_pixmap(alpha=True, matrix=mat).tobytes()
        image = Image.open(io.BytesIO(pixmap))
        image = image.resize((image.width*2, image.height*2))
        text = pytesseract.image_to_string(
            image, lang="ita", config=config)
        raw_string = text.rpartition('completato')[
            2].replace('\x0c', '').split('\n')
        comune = [i for i in raw_string if i]
        print(comune)

    print(textes)


pages = getPages('./download/'+latest['nome_file'])
#getIncidenza('./download/'+latest['nome_file'], pages['incidenza'])
getVax('./download/'+latest['nome_file'], pages['vaccini'])
