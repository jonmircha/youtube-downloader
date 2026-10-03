#!/bin/bash

# Obtener la ruta del directorio donde está este archivo
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

echo "=================================================="
echo "    🛠️  Setup & Diagnóstico - YouTube Downloader"
echo "=================================================="
echo ""

# 1. Verificar Python 3
echo "🔍 Verificando instalación de Python 3..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado."
    echo "Por favor, descarga e instala Python desde: https://www.python.org/downloads/"
    echo ""
    read -p "Presiona Enter para salir..."
    exit 1
fi
python3 --version
echo "✅ Python 3 está disponible."
echo ""

# 2. Verificar FFmpeg
echo "🔍 Verificando instalación de FFmpeg (requerido para audio MP3 y calidad HD)..."
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  FFmpeg no está instalado en el sistema."
    echo "yt-dlp necesita FFmpeg para convertir audio a MP3 y unir videos en HD."
    echo ""
    if command -v brew &> /dev/null; then
        echo "Homebrew está disponible en tu Mac."
        read -p "¿Deseas intentar instalar ffmpeg de forma automática con Homebrew? [s/n]: " respuesta
        if [[ "$respuesta" =~ ^[Ss]$ ]]; then
            echo "📥 Ejecutando 'brew install ffmpeg'..."
            brew install ffmpeg
        else
            echo "⚠️  Instalación omitida. Algunas funciones del downloader podrían fallar."
        fi
    else
        echo "Instrucciones de instalación manual en macOS:"
        echo "  1. Instala Homebrew (https://brew.sh/)"
        echo "  2. Ejecuta en tu terminal: brew install ffmpeg"
        echo "  O descárgalo directamente desde: https://ffmpeg.org/download.html"
    fi
else
    echo "✅ FFmpeg está instalado."
fi
echo ""

# 3. Crear/Reparar Entorno Virtual (.venv)
echo "🔍 Configurando el entorno virtual (.venv)..."
RECREAR_VENV=false

if [ ! -d ".venv" ]; then
    echo "📦 No se encontró el entorno virtual. Creando uno nuevo..."
    RECREAR_VENV=true
else
    # Verificar si el intérprete de Python y pip en .venv funcionan correctamente (detecta si se movió de carpeta)
    if ! .venv/bin/pip --version &> /dev/null; then
        echo "⚠️  El entorno virtual está roto o fue movido de carpeta. Recreando..."
        RECREAR_VENV=true
    fi
fi

if [ "$RECREAR_VENV" = true ]; then
    rm -rf .venv
    python3 -m venv .venv
    if [ $? -eq 0 ]; then
        echo "✅ Entorno virtual (.venv) creado correctamente."
    else
        echo "❌ Error al crear el entorno virtual."
        read -p "Presiona Enter para salir..."
        exit 1
    fi
else
    echo "✅ El entorno virtual (.venv) es válido."
fi
echo ""

# 4. Instalar/Actualizar Dependencias
# [default] incluye yt-dlp-ejs y [deno] el runtime de JavaScript: ambos son necesarios para YouTube
echo "📥 Instalando/actualizando dependencias (yt-dlp, yt-dlp-ejs, deno y certifi)..."
.venv/bin/pip install --upgrade pip
.venv/bin/pip install --upgrade "yt-dlp[default,deno]" certifi

if [ $? -eq 0 ]; then
    touch .venv/.ultima_actualizacion
    echo ""
    echo "🎉 ¡Configuración completada con éxito!"
    echo "El entorno ha sido reparado/configurado en esta ubicación."
else
    echo ""
    echo "⚠️  Hubo un problema al instalar las dependencias."
fi

echo ""
read -p "Presiona Enter para finalizar..."

# Cerrar la ventana de Terminal o salir de la aplicación si no hay otras ventanas abiertas
osascript -e 'tell application "Terminal"' \
          -e 'if (count of windows) > 1 then' \
          -e 'close front window' \
          -e 'else' \
          -e 'quit' \
          -e 'end if' \
          -e 'end tell' & exit
