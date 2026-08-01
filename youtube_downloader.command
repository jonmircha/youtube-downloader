#!/bin/bash

# Obtener la ruta del directorio donde está este archivo
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Cambiar a ese directorio
cd "$DIR"

# Verificar si el entorno virtual no existe o está dañado
VENV_OK=true
if [ ! -d ".venv" ]; then
    VENV_OK=false
elif ! .venv/bin/pip --version &> /dev/null; then
    VENV_OK=false
fi

# Si el entorno virtual no es válido, ejecutar el script de configuración automáticamente
if [ "$VENV_OK" = false ]; then
    echo "⚠️  Se detectó que el entorno virtual (.venv) no existe o está dañado."
    echo "Iniciando configuración/reparación automática..."
    echo ""
    ./setup.command
    
    # Comprobar nuevamente si se solucionó
    if [ ! -d ".venv" ] || ! .venv/bin/python3 -c "import sys" &> /dev/null; then
        echo "❌ No se pudo solucionar la configuración de forma automática."
        read -p "Presiona Enter para salir..."
        exit 1
    fi
fi

# Activar el entorno virtual
source .venv/bin/activate

# Ejecutar el script de Python
python3 youtube_downloader.py
STATUS=$?

if [ $STATUS -ne 0 ]; then
    echo ""
    echo "⚠️  El script finalizó con código de salida: $STATUS."
    read -p "Presiona Enter para cerrar esta ventana..."
fi

# Cerrar la ventana de Terminal o salir de la aplicación si no hay otras ventanas abiertas
osascript -e 'tell application "Terminal"' \
          -e 'if (count of windows) > 1 then' \
          -e 'close front window' \
          -e 'else' \
          -e 'quit' \
          -e 'end if' \
          -e 'end tell' & exit
