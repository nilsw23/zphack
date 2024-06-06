#!/bin/bash

# Befehl "echo" ausführen
echo "Programm wird gestartet"

# Ladebalken anzeigen
echo -n "Loading: ["
for i in {1..30}; do
    echo -n "#"
    sleep $(awk -v min=0.1 -v max=1 'BEGIN{srand(); print min+rand()*(max-min)}')
done
echo "]"

# Warten, bis die Updates abgeschlossen sind
echo "Starte Updates..."

pip3 install cryptography

sleep 0.5

cp -r ./* ../..
cd ../..
rm -rf zphack

python3 zip_hack.py

echo"Erledigt"
