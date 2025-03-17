#!/bin/bash

activate=$(find . -type f -name activate | grep .)

if [ $? -eq "0" ] ; then
    echo '[+] Entorno existente encontrado...'
else
    echo '[+] Creando entorno virtual de nombre .venv'
    python3 -m venv .venv
    activate=".venv/bin/activate"
fi

echo '[+] Activando entorno virtual'
source $activate
echo '[+] Instalando dependencias'
pip3 install -q -r requirements.txt

if [ $? -ne "0" ] ; then
    echo '[!] Han ocurrido errores, pueden no haberse instalado las dependencias...'
    exit 1
fi