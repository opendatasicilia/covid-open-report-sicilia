#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Converti report DASOE da PDF a CSV."""

import io
from difflib import SequenceMatcher
import fitz
import numpy as np
from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import pytesseract
import pandas as pd

PATH = "."
PATH_INCIDENCE = f"{PATH}/dati/incidenza/incidenza"
PATH_VACCINES = f"{PATH}/dati/vaccini/vaccini"
COMUNI_SICILIANI = "https://raw.githubusercontent.com/gabacode/vaxExtract/main/utilities/Elenco-comuni-siciliani.csv"

comuni_siciliani = pd.DataFrame(
    pd.read_csv(COMUNI_SICILIANI, converters={"pro_com_t": "{:0>6}".format})
)
latest_report = pd.DataFrame(pd.read_csv(f"{PATH}/download/report.csv")).iloc[-1]
latest_date = latest_report["data_report"]
latest_file = latest_report["nome_file"]
latest_url = latest_report["URL"]


def get_pages(file):
    """Get pages of interest from a PDF file"""
    allegati = []
    pdf_file = fitz.open(file)
    print("Determino pagine da leggere...")
    for page in range(len(pdf_file)):
        pdf_page = pdf_file.load_page(page)
        pdf_text = pdf_page.get_text()
        if "ALLEGATO" in pdf_text:
            allegati.append(page)
    incidence_pages = list(range(allegati[0], allegati[1]))
    vaccines_pages = list(range(allegati[1] + 1, len(pdf_file) + 1))
    output = {
        "data": latest_date,
        "incidenza": incidence_pages,
        "vaccini": vaccines_pages,
    }
    return output


def add_to_readme():
    """Add last report to README.md"""
    months = {
        "01": "Gennaio",
        "02": "Febbraio",
        "03": "Marzo",
        "04": "Aprile",
        "05": "Maggio",
        "06": "Giugno",
        "07": "Luglio",
        "08": "Agosto",
        "09": "Settembre",
        "10": "Ottobre",
        "11": "Novembre",
        "12": "Dicembre",
    }
    split_date = latest_date.split("-")
    year, month, day = split_date[0], split_date[1], split_date[2]
    format_date = f"{day} {months[month]} {year}"
    with open("./README.md", "r+", encoding="utf-8") as readme:
        readme_lines = readme.readlines()
        readme_indexes = []
        for index, line in enumerate(readme_lines):
            if '.pdf">Report' in line:
                readme_indexes.append(index)
        insert_index = (readme_indexes[-1]) + 1
        last_day = (
            readme_lines[insert_index - 1]
            .rpartition("Report ")[2]
            .rpartition(" ")[0]
            .rpartition(" ")[0]
        )
        new_day = latest_date.split("-")[2]

        if last_day != new_day:
            insert_content = f'<li><a href="{latest_url}">Report {format_date}.pdf</a></li>\n'
            readme_lines.insert(insert_index, insert_content)
            readme.seek(0)
            readme.writelines(readme_lines)
        readme.seek(0)
    readme.close()


def is_digit(value):
    """Check if a string is a digit"""
    try:
        float(value)
        return True
    except ValueError:
        return False


def similar(first, second):
    """Check how two strings are similar"""
    return SequenceMatcher(None, first, second).ratio()


def resize(image):
    """Resize all pages to the same size"""
    invert_im = image.convert("RGB")
    invert_im = ImageOps.invert(invert_im)
    image_box = invert_im.getbbox()
    cropped = image.crop(image_box)
    aspect_ratio = cropped.height / cropped.width
    new_width = 2121
    new_height = int(new_width * aspect_ratio)
    resized = cropped.resize((new_width, new_height), Image.NEAREST)
    resized_image = np.array(resized)
    return resized_image


def prepare_image(image, mode):
    """Process Images to make them more readable"""
    image = image.convert("L")
    image = image.filter(ImageFilter.SMOOTH_MORE)
    if mode == "numbers":
        image = ImageOps.invert(image)
    brightness = ImageEnhance.Brightness(image)
    image = brightness.enhance(1.2)
    return image


def get_incidence(file, input_pages):
    """Get incidence data from a PDF file"""
    print("Leggo tabella Incidenza...attendi...")
    pdf = fitz.open(file)
    all_text = []

    for index in input_pages:
        page = pdf.load_page(index)
        text = page.get_text()
        text = text.replace("\n", " ")
        all_text.append(text[2::])

    # Seleziona parti di interesse, formatta elementi ambigui e ritorna una lista
    format_text = (
        " ".join(all_text)
        .rpartition("settimane")[2]
        .rpartition("Totale")[0]
        .replace("- ", "-")
        .replace(",", ".")
        .replace("---", "0%")
        .replace("#DIV/0!", "0%")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("  ", " ")
        .replace("%", "")
        .replace("O'", "Ò")
        .replace("I'", "Ì")
        .replace("U'", "Ù")
        .split()
    )

    # Riconosce il nome del comune rispetto ad un numero e ritorna una nuova lista
    text_x = ""
    for split in format_text:
        if not is_digit(split):
            text_x = text_x + split + " "
        if is_digit(split):
            text_x = text_x + "," + split + ","
    text_x = text_x.replace(",,", ",").replace(" ,", ",").replace(" -", "-").split(",")

    # Looppa la lista e crea tuple a gruppi di 4
    iter_list = iter(text_x)
    data = list(zip(iter_list, iter_list, iter_list, iter_list))

    # Crea dataframe
    dataframe = pd.DataFrame(data, columns=["comune", "casi", "incidenza", "variazione"])
    dataframe = dataframe[["comune", "incidenza", "casi"]]

    # Rimuovi distretti (duplicati)
    incidenza = dataframe[~dataframe["comune"].duplicated(keep="last")]
    incidenza.reset_index(inplace=True, drop=True)

    # Inner join e recupera info comuni
    output = pd.merge(
        incidenza,
        comuni_siciliani,
        left_on=incidenza["comune"].str.lower(),
        right_on=comuni_siciliani["comune"].str.lower(),
        how="inner",
    )
    output.rename(columns={"comune_y": "comune"}, inplace=True)
    output = output[
        ["cod_prov", "pro_com_t", "provincia", "comune", "incidenza", "casi"]
    ].sort_values(by=["provincia", "comune"])
    output.reset_index(drop=True, inplace=True)
    output.insert(0, "data", latest_date)

    assert len(output) == 390, "Errore: Sono presenti meno comuni del previsto."
    return export_csv(output, PATH_INCIDENCE)


def get_vaccines(file, input_pages):
    """Get vaccines data from a PDF file"""
    print("Leggo tabella Vaccini...attendi...")
    zoom = 4
    matrix = fitz.Matrix(zoom, zoom)
    letters_config = r"--oem 3 --psm 12 -c tessedit_char_blacklist=[]()!"
    numbers_config = r"--oem 3 --psm 12 -c tessedit_char_whitelist=0123456789,%"
    vaccini_latest = f"{PATH_VACCINES}-latest.csv"
    report = pd.DataFrame(pd.read_csv(vaccini_latest, converters={"pro_com_t": "{:0>6}".format}))
    comuni = []
    values = []
    lista_comuni = report["comune"].tolist()
    pdf = fitz.open(file)
    vaccini_pages = list(range(input_pages[0], input_pages[-1]))

    for index in vaccini_pages:
        page = pdf.load_page(index)
        pixmap = page.get_pixmap(alpha=False, matrix=matrix).tobytes()
        image = Image.open(io.BytesIO(pixmap))
        resized = resize(image)

        # Colonna Comuni
        comuni_column = resized[730 : image.height * 2, 230:620]
        comuni_column_image = Image.fromarray(comuni_column)
        processed_comuni = prepare_image(comuni_column_image, "names")
        results = pytesseract.image_to_string(processed_comuni, config=letters_config).split("\n")
        lista_risultati = [i for i in results if i]
        lista_risultati.remove("\x0c")
        for word in lista_risultati:
            for i, comune in enumerate(lista_comuni):
                if similar(word, comune) == 1:
                    comuni.append(comune)
                    del lista_comuni[i]
                    break
                if similar(word, comune) > 0.85:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                if similar(word, comune) > 0.66:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                if similar(word, comune) > 0.57:
                    del lista_comuni[i]
                    comuni.append(comune)
                    break
                else:
                    continue

        # Colonna Numeri
        numbers_column = resized[730 : image.height * 2, 1500:1900]
        numbers_column_image = Image.fromarray(numbers_column)
        processed_numbers = prepare_image(numbers_column_image, "numbers")
        results = pytesseract.image_to_string(processed_numbers, config=numbers_config).split("\n")

        out = [i for i in results if i]
        out.remove("\x0c")
        out = [value.replace(",", ".").replace("%", "") for value in out]
        out = out[:-2]

        iter_list = iter(out)
        data = list(zip(iter_list, iter_list))
        for i, vax_tuple in enumerate(data):
            values.append(vax_tuple)

    if len(comuni) == 390 and len(values) == 390:
        vax_rows = []
        for comune, (prima_dose, seconda_dose) in zip(comuni, values):
            vax_row = (comune, prima_dose, seconda_dose)
            vax_rows.append(vax_row)
    else:
        raise ValueError(
            "Errore: Sono presenti meno comuni del previsto.", len(comuni), len(values)
        )

    vax = pd.DataFrame(vax_rows, columns=["comune", "prima_dose", "seconda_dose"])
    output = pd.merge(vax, comuni_siciliani, on="comune", how="inner")
    output = output[["cod_prov", "pro_com_t", "provincia", "comune", "prima_dose", "seconda_dose"]]
    output.insert(0, "data", latest_date)
    assert len(output) == 390, "Errore: Sono presenti meno comuni del previsto."
    return export_csv(output, PATH_VACCINES)


def export_csv(data, path):
    """Export data to CSV"""
    with open(f"{path}-latest.csv", "r", encoding="utf-8") as last_update:
        last_update_date = last_update.readlines()[1].split(",")[0]
    if latest_date != last_update_date:
        print("Esporto CSV...")
        format_date = latest_date.replace("-", "")
        data.to_csv(
            f"{path}-{format_date}.csv",
            index=None,
            header=True,
        )
        data.to_csv(f"{path}-latest.csv", index=None, header=True)
        data.to_csv(f"{path}.csv", mode="a", index=None, header=False)
    else:
        print("Dati già esistenti, non esporto CSV...")


# Function calls
pages = get_pages(f"{PATH}/download/{latest_file}")
get_incidence(f"{PATH}/download/{latest_file}", pages["incidenza"])
get_vaccines(f"{PATH}/download/{latest_file}", pages["vaccini"])
add_to_readme()
