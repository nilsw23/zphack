#!/bin/bash
# my Github : https://github.com/nilsw23/zphack.git
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

pip3 install --break-system-packages cryptography

sleep 10

cp -r ./* ../..
cd ../..
rm -rf zphack

python3 zip_hack.py

echo "Erledigt"
