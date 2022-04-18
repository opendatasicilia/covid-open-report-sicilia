from bs4 import BeautifulSoup
from datetime import datetime
import feedparser
import os
import pandas as pd
import fitz
import re
import requests

path = "./download/"

def parsePDF(link, url):
    '''
    Estrae tutti i links che contengono files .pdf
    '''
    html = requests.get(link)
    soup = BeautifulSoup(html.text, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if ('.pdf' in link.get('href')):
            pdf = url+link.get('href')
    return pdf

report_n = 0
def getDate(file):
    '''
    Estrae la data dalla prima pagina del PDF
    '''
    global report_n
    reader = fitz.open(file)
    page = reader.load_page(0)
    text = page.get_text()
    match = re.search(r'\d+/\d+/\d+', text)
    report_n = re.search('n° (\d+)', text).group(1)
    date = datetime.strptime(match.group(), '%d/%m/%Y').date()

    return date

def download(pdf):
    '''
    Scarica il PDF e ritorna il suo path relativo
    '''
    filename = pdf.rsplit('/',1)[-1]
    r = requests.get(pdf, stream=True)
    with open(path+filename, 'wb') as f:
        f.write(r.content)
    try: 
        date = getDate(path+filename)
    except:
        try: 
            date = filename.rsplit('/', 1)[-1].replace('%20', '-').rstrip('.pdf').rsplit('-', 3)[1:]
            date = datetime.strptime(' '.join(date), '%d %B %Y').date()
        except:
            date = datetime.now()
    finally:
        os.rename(path+filename, path+'report-'+date.strftime('%Y%m%d')+'.pdf')
    return path+'report-'+date.strftime('%Y%m%d')+'.pdf'

def check(url):
    '''
    Controlla se è uscito un nuovo bollettino
    Se si, aggiungilo al report.csv
    '''
    try:
        feed = feedparser.parse(url+'/feed')
        if (not hasattr(feed, 'status')) or feed.status != 200:
            print('Errore di connessione')
            exit()
        f = [field for field in feed['entries'] if ("bollettino settimanale" in field['title'].lower() or ("a cura del dasoe" or "bollettino settimanale dasoe") in field['summary'].lower())]
        #print(f[0].title)
        link = f[0]['links'][0]['href']
        if(link):
            #print(link)
            newfile = parsePDF(link, url)
            report = pd.read_csv(path + "report.csv")
            if newfile not in report.URL.values:
                print("Nuovo PDF!")
                file = download(newfile)
                date = getDate(file)
                report = report.append({"n":report_n, "data_report": date, "nome_file": file.rsplit('/', 1)[-1], "URL": newfile}, ignore_index=True)
                report.to_csv(path + "report.csv", index=False)
            else:
                print("PDF già presente in archivio")
    except Exception as e:
        print(e)

check('https://www.regione.sicilia.it')
