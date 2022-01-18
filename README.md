⚠️ Se vuoi rimanere aggiornato, ti puoi iscrivere al [feed RSS dei ChangeLog](https://github.com/opendatasicilia/covid-open-report-sicilia/commits/main/CHANGELOG.md.atom)

# COVID open report Sicilia
[![Frictionless](https://github.com/opendatasicilia/covid-open-report-sicilia/actions/workflows/frictionless.yaml/badge.svg)](https://repository.frictionlessdata.io/report?user=opendatasicilia&repo=covid-open-report-sicilia&flow=frictionless) [![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/) <a href="https://www.datibenecomune.it/"><img src="https://img.shields.io/badge/%F0%9F%99%8F-%23datiBeneComune-%23cc3232"/></a>

Dal 6 ottobre 2021 il Dipartimento Attività Sanitarie e Osservatorio Epidemiologico (DASOE) della Regione Siciliana rilascia bollettini settimanali (in formato PDF) ai quali sono allegate due tabelle contenenti **dati epidemiologici e vaccinali con dettaglio comunale**. Le tabelle allegate vengono convertite in CSV e caricate nella cartella [`dati`](https://github.com/opendatasicilia/covid-open-report-sicilia/tree/main/dati) di questo repo.

Gli stessi dati alimentano:
- 📍 API endpoints documentati e raggiungibili al [seguente link](https://covid-open-report-sicilia.herokuapp.com/);
- 📊 dashboard interattiva raggiungibile al [seguente link](https://report-dasoe.opendatasicilia.it/).

![covid-open-report-sicilia](https://user-images.githubusercontent.com/77018886/143773850-a0f79d60-77e3-4a8c-bb82-5553c85c0bcf.png)

## Bollettini pubblicati
- [Report 06 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2006%20Ottobre%202021.pdf)
- [Report 13 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2013%20Ottobre%202021.pdf)
- [Report 20 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2020%20Ottobre%202021.pdf)
- [Report 27 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2027%20Ottobre%202021.pdf)
- [Report 04 Novembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20n%C3%82%C2%B0%205%20del%204%20novembre.pdf)
- [Report 10 Novembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20settimanale%20n%C2%B06%20del%2010%20novembre%202021.pdf)
- [Report 17 Novembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20Dasoe%207%20del%2017%20Novembre%202021.pdf)
- [Report 24 Novembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20n.8%20del%2024%20novembre%202021.pdf)
- [Report 01 Dicembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20settimanale%201%20dicembre%20%282%29.pdf)
- [Report 08 Dicembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%2008%20Dicembre%202021.pdf)
- [Report 15 Dicembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20Dasoe%20n.11%20del%2015%20Dicembre%202021.pdf)
- [Report 22 Dicembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20Dasoe%2012%20del%2022%20Dicembre%202021.pdf)
- [Report 29 Dicembre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20Dasoe%2013%20del%2029%20dicembre%202021.pdf)
- [Report 06 Gennaio 2022.pdf](https://www.regione.sicilia.it/sites/default/files/2022-01/bollettino%2014%20finale.pdf)
- [Report 12 Gennaio 2022.pdf](https://www.regione.sicilia.it/sites/default/files/2022-01/Bollettino%2012%20gennaio%202022.pdf)

## Struttura repository
```
covid-open-report-sicilia
├── 📂dati
│   ├── 📂incidenza
│   │   ├── 📄incidenza-YYYYMMDD.csv
│   │   ├── 📄incidenza-latest.csv
│   │   └── 📄incidenza.csv
│   └── 📂vaccini
│       ├── 📄vaccini-YYYYMMDD.csv
│       ├── 📄vaccini-latest.csv
│       └── 📄vaccini.csv
├── 📂download
│   ├── 📄report.csv
│   └── 📄report-YYYYMMDD.pdf
├── 📂script
│   ├── 📄script.sh
│   └── 📄script.py
└── 📂api
```

## Schema dati
- metadata: [datapackage.yaml](https://github.com/opendatasicilia/covid-open-report-sicilia/blob/main/datapackage.yaml)
### Dati per comune relativi a incidenza e nuovi casi settimanali

- Directory:  dati/incidenza<br>
- Struttura file settimanale: `incidenza-YYYYMMDD.csv`<br>
- File complessivo: `incidenza.csv`<br>
- File ultimi dati (latest): `incidenza-latest.csv`
- Encoding: `UTF-8`
- Separatore di campo: `,`

Campo | Descrizione | Formato | Esempio
-- | -- | -- | --
data | Data pubblicazione report DASOE | YYYY-MM-DD | 2021-10-27
cod_prov | Codice ISTAT della Provincia | Numero | 84
pro_com_t | Codice ISTAT del Comune | Testo | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
incidenza | Incidenza cumulativa settimanale (ogni 100.000 abitanti) | Numero | 855
casi | Nuovi casi settimanali | Numero | 6

### Dati per comune relativi a persone vaccinate

- Directory:  dati/vaccini<br>
- Struttura file settimanale: `vaccini-YYYYMMDD.csv`<br>
- File complessivo: `vaccini.csv`<br>
- File ultimi dati (latest): `vaccini-latest.csv`
- Encoding: `UTF-8`
- Separatore di campo: `,`

Campo | Descrizione | Formato | Esempio
-- | -- | -- | --
data | Data pubblicazione report DASOE | YYYY-MM-DD | 2021-10-27
cod_prov | Codice ISTAT della Provincia | Numero | 84
pro_com_t | Codice ISTAT del Comune | Testo | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
prima_dose | Percentuale di persone vaccinate con almeno una dose (calcolata rispetto al target) | Numero | 84.65
seconda_dose | Percentuale di: persone vaccinate con 2 o più dosi, persone vaccinate in monodose per pregressa infezione Covid, persone vaccinate con Janssen (calcolata rispetto al target) | Numero | 82.72

**Nota bene:**
- Dal [Bollettino n°4](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20n%C3%82%C2%B0%205%20del%204%20novembre.pdf) si apprende che _Per target si intende la popolazione residente ISTAT 2021 DI Età >= 12 ANNI._
- Dal [Bollettino n°12](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20Dasoe%2012%20del%2022%20Dicembre%202021.pdf) si apprende che a partire dal [Bollettino n° 11 del 15/12/2021](https://www.regione.sicilia.it/sites/default/files/2021-12/Bollettino%20Dasoe%20n.11%20del%2015%20Dicembre%202021.pdf) gli allegati relativi alla vaccinazione contemplano _il target 5-11 anni quale platea avente diritto alla vaccinazione, con un conseguente decremento della % di popolazione immunizzata per singolo comune._ Pertanto è possibile stimare il numero assoluto di persone vaccinate utilizzando [questo file json.](https://raw.githubusercontent.com/opendatasicilia/cors-dashboard/main/src/data/targets.json)

## Licenza
<a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/CC-BY_icon.svg/640px-CC-BY_icon.svg.png" width="150"/></a>

## Elaborazioni
Dati aperti di questo tipo consentono la realizzazione di svariate elaborazioni:
- [Report settimanale interattivo](https://report-dasoe.opendatasicilia.it/) di [Open Data Sicilia](https://opendatasicilia.it) ([GitHub](https://github.com/opendatasicilia/cors-dashboard))
- [Sintesi Bollettino settimanale: Dati Epidemiologici e Vaccinali](https://opendatasicilia.github.io/OpenDataSicilia-per-il-Coronavirus/vaccini/report_sintesi/) di [Giovan Battista Vitrano](https://twitter.com/gbvitrano)
- [MONIVAX - Monitora i vaccinati della tua città](https://github.com/opendatasicilia/monivax) di [Giovanni Pirrotta](https://twitter.com/gpirrotta)
