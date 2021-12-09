<a href="https://www.datibenecomune.it/"><img src="https://img.shields.io/badge/%F0%9F%99%8F-%23datiBeneComune-%23cc3232"/></a>
# COVID open report Sicilia
Dal 6 ottobre 2021 il Dipartimento Attività Sanitarie e Osservatorio Epidemiologico (DASOE) della Regione Siciliana rilascia bollettini settimanali (in formato PDF) ai quali sono allegate due tabelle contenenti **dati epidemiologici e vaccinali con dettaglio comunale**. Le tabelle allegate vengono convertite in CSV e caricate nella cartella [`dati`](https://github.com/opendatasicilia/covid-open-report-sicilia/tree/main/dati) di questo repo.

Gli stessi dati alimentano gli API endpoints documentati e raggiungibili al [seguente link](https://covid-open-report-sicilia.herokuapp.com/).

![covid-open-report-sicilia](https://user-images.githubusercontent.com/77018886/143773850-a0f79d60-77e3-4a8c-bb82-5553c85c0bcf.png)

### Bollettini pubblicati
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
│   ├── 📄report.csv
│   └── 📄report-YYYYMMDD.pdf
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
pro_com_t | Codice ISTAT del Comune | Testo | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
incidenza | Incidenza cumulativa settimanale (ogni 100.000 abitanti) | Numero | 855
casi | Nuovi casi settimanali | Numero | 6

#### Struttura file `vaccini-YYYYMMDD.csv`, `vaccini-latest.csv`, `vaccini.csv`

Campo | Descrizione | Formato | Esempio
-- | -- | -- | --
data | Data pubblicazione report DASOE | YYYY-MM-DD | 2021-10-27
cod_prov | Codice ISTAT della Provincia | Numero | 84
pro_com_t | Codice ISTAT del Comune | Testo | 084002
provincia | Denominazione della Provincia | Testo | Agrigento
comune | Denominazione del Comune | Testo | Alessandria della Rocca
%vaccinati | Percentuale di persone vaccinate con almeno una dose (calcolata rispetto al target) | Numero | 84.65
%immunizzati | Percentuale di: persone vaccinate con 2 o più dosi, persone vaccinate in monodose per pregressa infezione Covid, persone vaccinate con Janssen (calcolata rispetto al target) | Numero | 82.72

**Nota bene:**
Dal [Bollettino n°4](https://www.regione.sicilia.it/sites/default/files/2021-11/Bollettino%20n%C3%82%C2%B0%205%20del%204%20novembre.pdf) si apprende che _Per target si intende la popolazione residente ISTAT 2021 DI Età >= 12 ANNI_ quindi è possibile stimare il numero assoluto di persone vaccinate utilizzando [questo file](https://raw.githubusercontent.com/opendatasicilia/comuni-italiani/main/dati/ISTAT_popolazione_2021.csv).

### Licenza
<a href="https://creativecommons.org/licenses/by/4.0/"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/16/CC-BY_icon.svg/640px-CC-BY_icon.svg.png" width="150"/></a>

## Elaborazioni
Dati aperti di questo tipo consentono la realizzazione di svariate elaborazioni:
- [Sintesi Bollettino settimanale n° 3 del 20/10/2021: Dati Epidemiologici e Vaccinali](https://opendatasicilia.github.io/OpenDataSicilia-per-il-Coronavirus/vaccini/report_03/) di [Giovan Battista Vitrano](https://twitter.com/gbvitrano)
- [Sintesi Bollettino settimanale n° 4 del 27/10/2021: Dati Epidemiologici e Vaccinali](https://opendatasicilia.github.io/OpenDataSicilia-per-il-Coronavirus/vaccini/report_04/) di [Giovan Battista Vitrano](https://twitter.com/gbvitrano)
- [Sintesi Bollettino settimanale n° 5 del 04/11/2021: Dati Epidemiologici e Vaccinali](https://opendatasicilia.github.io/OpenDataSicilia-per-il-Coronavirus/vaccini/report_05/) di [Giovan Battista Vitrano](https://twitter.com/gbvitrano)
- [Report settimanale intereattivo (bozza)](https://datastudio.google.com/u/1/reporting/7f0563bf-c15d-4070-b37e-e986ec0edd09/page/zFUeC) di [Dennis Angemi](https://twitter.com/dennisangemi)
