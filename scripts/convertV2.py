#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import fitz
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract
import pandas as pd
from difflib import SequenceMatcher

path = '.'
comuni_siciliani = pd.DataFrame(pd.read_csv(
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
    # print(output)
    return output


def addToReadme():
    '''
    Aggiunge ultima riga del report.csv al file README.md
    '''
    mesi = {"01": "Gennaio", "02": "Febbraio", "03": "Marzo", "04": "Aprile", "05": "Maggio", "06": "Giugno",
            "07": "Luglio", "08": "Agosto", "09": "Settembre", "10": "Ottobre", "11": "Novembre", "12": "Dicembre"}
    data = date.split('-')
    data = data[2] + " " + mesi[data[1]] + " " + data[0]
    with open("./README.md", "r+", encoding="utf-8") as f:
        lines = f.readlines()
        lindex = []
        for index, line in enumerate(lines):
            if '.pdf">Report' in line:
                lindex.append(index)
        insert_index = (lindex[-1]) + 1
        lastDay = lines[insert_index -
                        1].rpartition('Report ')[2].rpartition(' ')[0].rpartition(' ')[0]
        newDay = date.split('-')[2]
        if lastDay != newDay:
            insert_content = '<li><a href="' + \
                latest['URL'] + '">Report ' + data + '.pdf</a></li>\n'
            lines.insert(insert_index, insert_content)
            f.seek(0)
            f.writelines(lines)
        f.seek(0)
    f.close()


def isDigit(x):
    '''
    True se x contiene un numero
    '''
    try:
        float(x)
        return True
    except ValueError:
        return False


def similar(a, b):
    '''Check how similar are two strings'''
    return SequenceMatcher(None, a, b).ratio()


def resize(image):
    '''Resize all pages to the same size'''
    invert_im = image.convert("RGB")
    invert_im = ImageOps.invert(invert_im)
    imageBox = invert_im.getbbox()
    cropped = image.crop(imageBox)
    aspect_ratio = cropped.height / cropped.width
    new_width = 2121
    new_height = int(new_width * aspect_ratio)
    resized = cropped.resize((new_width, new_height), Image.NEAREST)
    resized_image = np.array(resized)
    return resized_image


def prepare(image, mode):
    '''Process Images to make them more readable'''
    image = image.convert('L')
    image = image.filter(ImageFilter.SMOOTH_MORE)
    if mode == 'numbers':
        image = ImageOps.invert(image)
    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(1.2)
    return image


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
    out = pd.merge(incidenza, comuni_siciliani, left_on=incidenza["comune"].str.lower(
    ), right_on=comuni_siciliani["comune"].str.lower(), how="inner")
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
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    letters_config = r'--oem 3 --psm 12 -c tessedit_char_blacklist=[]()!'
    numbers_config = r'--oem 3 --psm 12 -c tessedit_char_whitelist=0123456789,%'
    report = pd.DataFrame(pd.read_csv(
        'https://raw.githubusercontent.com/opendatasicilia/covid-open-report-sicilia/main/dati/vaccini/vaccini-latest.csv', converters={'pro_com_t': '{:0>6}'.format}))
    comuni = []
    values = []
    lista_comuni = report['comune'].tolist()
    pdf = fitz.open(file)
    for index in range(pages[0], pages[-1]):
        page = pdf.load_page(index)
        pixmap = page.get_pixmap(alpha=False, matrix=mat).tobytes()
        image = Image.open(io.BytesIO(pixmap))
        resized = resize(image)

        # Colonna Comuni
        comuni_column = resized[730:image.height*2, 230:620]
        comuni_column_image = Image.fromarray(comuni_column)
        processed_comuni = prepare(comuni_column_image, 'names')
        results = pytesseract.image_to_string(
            processed_comuni, config=letters_config).split('\n')
        lista_risultati = [i for i in results if i]
        lista_risultati.remove('\x0c')
        for item in lista_risultati:
            for i, comune in enumerate(lista_comuni):
                if similar(item, comune) == 1:
                    comuni.append(comune)
                    del lista_comuni[i]
                    break
                elif similar(item, comune) > 0.85:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                elif similar(item, comune) > 0.66:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                elif similar(item, comune) > 0.57:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                else:
                    continue

        # Colonna Numeri
        numbers_column = resized[730:image.height*2, 1500:1900]
        numbers_column_image = Image.fromarray(numbers_column)
        processed_numbers = prepare(numbers_column_image, 'numbers')
        results = pytesseract.image_to_string(
            processed_numbers, config=numbers_config).split('\n')

        out = [i for i in results if i]
        out.remove('\x0c')
        out = [value.replace(',', '.').replace('%', '') for value in out]
        out = out[:-2]

        it = iter(out)
        data = list(zip(it, it))
        for index, tuple_ in enumerate(data):
            values.append(tuple_)

    if len(comuni) == 390 and len(values) == 390:
        vax_tuples = []
        for comune, (prima_dose, seconda_dose) in zip(comuni, values):
            vax_tuples.append((comune, prima_dose, seconda_dose))
    else:
        print('nope')
        exit()

    vax = pd.DataFrame(vax_tuples, columns=[
                       'comune', 'prima_dose', 'seconda_dose'])
    out = pd.merge(vax, comuni_siciliani, on='comune', how='inner')
    out = out[['cod_prov', 'pro_com_t', 'provincia',
               'comune', 'prima_dose', 'seconda_dose']]
    out.insert(0, 'data', date)
    assert (len(out) == 390), "Errore: Sono presenti meno comuni del previsto."
    # print(out)
    lastUpdate = open(
        path+'/dati/vaccini/vaccini.csv').read().rsplit('\n', 2)[1].split(',')[0]
    if date != lastUpdate:
        print('Esporto CSV...')
        out.to_csv(path+'/dati/vaccini/vaccini-' +
                   date.replace("-", "")+'.csv', index=None, header=True)
        out.to_csv(path+'/dati/vaccini/vaccini-latest.csv',
                   index=None, header=True)
        out.to_csv(path+'/dati/vaccini/vaccini.csv',
                   mode='a', index=None, header=False)
    csv = path+'/dati/vaccini/vaccini-'+date.replace("-", "")+'.csv'
    return csv


pages = getPages('./download/'+latest['nome_file'])
getIncidenza('./download/'+latest['nome_file'], pages['incidenza'])
getVax('./download/'+latest['nome_file'], pages['vaccini'])
addToReadme()
