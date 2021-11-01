<a href="https://www.datibenecomune.it/"><img src="https://img.shields.io/badge/%F0%9F%99%8F-%23datiBeneComune-%23cc3232"/></a>
# COVID open report Sicilia
Dal 6 ottobre 2021 il Dipartimento Attività Sanitarie e Osservatorio Epidemiologico (DASOE) della Regione Siciliana rilascia bollettini settimanali (in formato PDF) ai quali sono allegate due tabelle contenenti **dati epidemiologici e vaccinali con dettaglio comunale**. Le tabelle allegate vengono convertite in CSV e caricate nella cartella [`dati`](https://github.com/opendatasicilia/covid-open-report-sicilia/tree/main/dati) di questo repo.

Gli stessi dati alimentano gli API endpoints documentati e raggiungibili al [seguente link](https://covid-open-report-sicilia.herokuapp.com/).

### Bollettini pubblicati
- [Report Completo 06 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2006%20Ottobre%202021.pdf)
- [Report Completo 13 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2013%20Ottobre%202021.pdf)
- [Report Completo 20 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2020%20Ottobre%202021.pdf)
- [Report Completo 27 Ottobre 2021.pdf](https://www.regione.sicilia.it/sites/default/files/2021-10/Report%20Completo%2027%20Ottobre%202021.pdf)

### Struttura repository
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
│   └── 📄Report Completo DD MMMM YYYY.pdf
├── 📂script
│   ├── 📄script.sh
│   └── 📄script.py
└── 📂api
```

### Schema dati
#### Struttura file `incidenza-YYYYMMDD.csv`, `incidenza-latest.csv`, `incidenza.csv`

Campo | Descrizione | Formato | Esempio
-- | -- | -- | --
data | Data pubblicazione report DASOE | YYYY-MM-DD | 2021-10-27
cod_prov | Codice ISTAT della Provincia | Numero | 84
pro_com_t | Codice ISTAT del Comune | Numero | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
incidenza | Incidenza cumulativa settimanale (ogni 100.000 abitanti) | Numero | 855
casi | Nuovi casi settimanali | Numero | 6

#### Struttura file `vaccini-YYYYMMDD.csv`, `vaccini-latest.csv`, `vaccini.csv`

Campo | Descrizione | Formato | Esempio
-- | -- | -- | --
data | Data pubblicazione report DASOE | YYYY-MM-DD | 2021-10-27
cod_prov | Codice ISTAT della Provincia | Numero | 84
pro_com_t | Codice ISTAT del Comune | Numero | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
target | Popolazione ISTAT 2021 over 12 | Numero | 2426
%vaccinati | Percentuale di persone vaccinate con almeno una dose (calcolata rispetto al target) | Numero | 84.65
%immunizzati | Percentuale di: persone vaccinate con 2 o più dosi, persone vaccinate in monodose per pregressa infezione Covid, persone vaccinate con Janssen (calcolata rispetto al target) | Numero | 82.72

### Licenza
<a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/CC-BY_icon.svg/640px-CC-BY_icon.svg.png" width="150"/></a>

## Elaborazioni
Dati aperti di questo tipo consentono la realizzazione di svariate elaborazioni:
- [Sintesi Bollettino settimanale n° 4 del 27/10/2021: Dati Epidemiologici e Vaccinali](https://opendatasicilia.github.io/OpenDataSicilia-per-il-Coronavirus/vaccini/report_04/) di [Giovan Battista Vitrano](https://twitter.com/gbvitrano)
