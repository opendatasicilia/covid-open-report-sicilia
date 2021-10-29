# COVID open report Sicilia
Dal 6 ottobre 2021 il Dipartimento Attività Sanitarie e Osservatorio Epidemiologico (DASOE) della Regione Siciliana rilascia bollettini settimanali (in formato PDF) ai quali sono allegate due tabelle contenenti dati epidemiologici e vaccinali con dettaglio comunale. Le tabelle allegate verranno convertite in CSV e caricate nella cartella `dati` di questo repo.

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
│   │   ├── 📄incidenzaYYYYMMDD.csv
│   │   ├── 📄incidenza_latest.csv
│   │   └── 📄incidenza.csv
│   └── 📂vaccini
│       ├── 📄vacciniYYYYMMDD.csv
│       ├── 📄vaccini_latest.csv
│       └── 📄vaccini.csv
├── 📂download
│   └── 📄Report Completo DD MMMM YYYY.pdf
├── 📂script
│   ├── 📄script.sh
│   └── 📄script.py
└── 📂api
```

### Schema dati
