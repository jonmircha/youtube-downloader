# 🎬 YouTube Downloader con yt-dlp

Una herramienta ligera, interactiva y automatizada para descargar videos de YouTube en formato MP4 (en varias resoluciones) o extraer solo el audio en formato MP3 con alta calidad.

El proyecto está optimizado especialmente para macOS, permitiendo su ejecución directa haciendo doble clic en un archivo instalable/ejecutable `.command`.

---

## 🚀 Características principales
- **Descarga interactiva**: Solicita la URL del video y te muestra la información antes de descargar (título, duración, canal, visualizaciones).
- **Formatos disponibles**:
  - 🎵 **Solo audio (MP3)**: Extrae el audio del video y lo convierte a formato MP3 a 192 kbps.
  - 🎬 **Video completo (MP4)**: Descarga en calidad seleccionable: 1080p (Full HD), 720p (HD), 480p (SD) o la máxima calidad disponible.
- **Autodiagnóstico y Auto-reparación**: Si mueves la carpeta de ubicación o tu entorno de Python cambia, la herramienta detecta de forma automática que el entorno virtual está roto y lo repara/actualiza antes de correr.
- **Cierre de terminal controlado**: Al finalizar, cierra la ventana de la terminal y finaliza el proceso de Terminal (si no hay otras ventanas abiertas). Si ocurre un error, mantiene la ventana abierta hasta que presiones Enter para que puedas leer el diagnóstico.

---

## 🛠️ Requisitos previos

Para que el descargador funcione correctamente en tu computadora, necesitas dos herramientas fundamentales:

1. **Python 3.10 o superior**: El lenguaje en el que está escrito el descargador.
2. **FFmpeg**: Un codificador de multimedia esencial que `yt-dlp` utiliza en segundo plano para convertir audio a MP3 y para unir las pistas de video y audio en alta definición (1080p+).

---

## 📦 Estructura del proyecto

El proyecto contiene los siguientes archivos principales:

- 📄 [youtube_downloader.py](file:///Users/jonmircha/Sync/My/Taller/youtube-downloader/youtube_downloader.py): Código lógico en Python que realiza las consultas a la API de YouTube y gestiona las descargas usando `yt-dlp`.
- ⚙️ [youtube_downloader.command](file:///Users/jonmircha/Sync/My/Taller/youtube-downloader/youtube_downloader.command): Acceso directo ejecutable en macOS para iniciar el descargador con un doble clic.
- 🛠️ [setup.command](file:///Users/jonmircha/Sync/My/Taller/youtube-downloader/setup.command): Script de autodiagnóstico que verifica e instala Python 3, FFmpeg, crea el entorno virtual `.venv` e instala las dependencias (`yt-dlp` y `certifi`).
- 📁 `.venv/`: Directorio autogenerado que contiene el entorno virtual aislado con las dependencias necesarias.

---

## 💻 Instalación y Configuración

Puedes realizar todo el diagnóstico e instalación de forma completamente automática.

### Método Automático (Recomendado en macOS)
Simplemente haz doble clic sobre el archivo [setup.command](file:///Users/jonmircha/Sync/My/Taller/youtube-downloader/setup.command).

El script realizará las siguientes comprobaciones y acciones:
1. **Verificará Python 3**: Si no lo tienes, te guiará para descargarlo.
2. **Verificará FFmpeg**: Si no está instalado pero tienes Homebrew, te ofrecerá instalarlo automáticamente ejecutando `brew install ffmpeg`.
3. **Creará/Reparará el Entorno Virtual (`.venv`)**: Si no existe o fue dañado al mover la carpeta, lo reconstruirá de cero.
4. **Instalará las dependencias**: Descargará las últimas versiones estables de `yt-dlp` y `certifi`.

---

## 📖 Instrucciones de Uso

Una vez completada la configuración previa:

1. Haz doble clic en [youtube_downloader.command](file:///Users/jonmircha/Sync/My/Taller/youtube-downloader/youtube_downloader.command).
2. Pega la **URL** del video de YouTube que quieres descargar y presiona `Enter`.
3. Revisa la información del video mostrada en pantalla.
4. Elige una opción:
   - Presiona `1` para extraer el **audio en MP3**.
   - Presiona `2` para descargar el **video completo en MP4** (luego te solicitará seleccionar la calidad deseada).
5. Especifica la **carpeta de destino** donde deseas guardar el archivo (presiona `Enter` para guardarlo en la carpeta de descargas de tu usuario `~/Downloads`).
6. Una vez que termine la descarga, la ventana de la terminal se cerrará de forma automática.

---

## 🔄 ¿Qué pasa si muevo la carpeta del proyecto?

Los entornos virtuales de Python guardan rutas absolutas en sus archivos binarios. Si mueves la carpeta de este proyecto a otro directorio o disco:
- **No te preocupes:** Al hacer doble clic en `youtube_downloader.command`, el script detectará de forma automática que la ruta del entorno virtual se ha roto y lanzará el asistente `setup.command` en segundo plano para repararse a sí mismo en la nueva ubicación.
