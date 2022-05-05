"""Controlla se è uscito un nuovo bollettino"""

import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
import feedparser
import pandas as pd
import fitz
import requests

PATH_DOWNLOAD = "./download"


def parse_pdf(post_link, url):
    """
    Estrae tutti i links che contengono files .pdf
    """
    html = requests.get(post_link)
    body = BeautifulSoup(html.text, "html.parser")
    links = body.find_all("a")
    for link in links:
        if ".pdf" in link.get("href"):
            return url + link.get("href")
    return None


def get_report(file):
    """
    Estrae dati report dalla prima pagina del PDF
    """
    reader = fitz.open(file)
    first_page = reader.load_page(0)
    page_text = first_page.get_text()
    date_match = re.search(r"\d+/\d+/\d+", page_text)
    report_number = re.search("n° (\\d+)", page_text).group(1)
    report_date = datetime.strptime(date_match.group(), "%d/%m/%Y").date()
    return {
        "number": report_number,
        "date": report_date,
    }


def download(pdf):
    """
    Scarica il PDF e ritorna il suo path relativo
    """
    filename = pdf.rsplit("/", 1)[-1]
    request = requests.get(pdf, stream=True)
    file_path = PATH_DOWNLOAD + "/" + filename
    with open(file_path, "wb") as file:
        file.write(request.content)
        report = get_report(file_path)
        report_date = report["date"].strftime("%Y%m%d")
        os.rename(file_path, f"{PATH_DOWNLOAD}/report-{report_date}.pdf")
    return f"{PATH_DOWNLOAD}/report-{report_date}.pdf"


def check(url):
    """
    Se è uscito un nuovo bollettino aggiungilo al report.csv
    """
    try:
        feed = feedparser.parse(url + "/feed")
        if (not hasattr(feed, "status")) or feed.status != 200:
            raise SystemExit("Errore di connessione")
        post_element = [
            field
            for field in feed["entries"]
            if (
                "bollettino settimanale" in field["title"].lower()
                or ("a cura del dasoe" or "bollettino settimanale dasoe")
                in field["summary"].lower()
            )
        ]
        post_link = post_element[0]["links"][0]["href"]
        if post_link:
            report_url = parse_pdf(post_link, url)
            reports = pd.read_csv(PATH_DOWNLOAD + "/report.csv")
            if report_url not in reports["URL"].values:
                print("Nuovo PDF!")
                new_file = download(report_url)
                report = get_report(new_file)
                report_date = report["date"]
                report_number = report["number"]
                reports = reports.append(
                    {
                        "n": report_number,
                        "data_report": report_date,
                        "nome_file": new_file.rsplit("/", 1)[-1],
                        "URL": report_url,
                    },
                    ignore_index=True,
                )
                reports.to_csv(PATH_DOWNLOAD + "/report.csv", index=False)
            else:
                print("PDF già presente in archivio")
    except ConnectionError as error:
        print(error)


check("https://www.regione.sicilia.it")
