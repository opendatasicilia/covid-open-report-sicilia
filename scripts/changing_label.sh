#!/bin/bash

# This script will change the label of the fields '%immunizzati' and '%vaccinati' of every csv file in the dati/vaccini directory

# Rename '%vaccinati' to '%prima_dose' and '%immunizzati' to '%seconda_dose'
for file in ../dati/vaccini/*.csv
do
    echo "Processing $file"
    sed 's/%vaccinati/prima_dose/' $file > ${file}_new.csv
    mv ${file}_new.csv $file
    sed 's/%immunizzati/seconda_dose/' $file > ${file}_new.csv
    mv ${file}_new.csv $file
done