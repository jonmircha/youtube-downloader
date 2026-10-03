# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Contexto

CLI interactiva en Python que descarga videos de YouTube como MP4 o extrae el audio como MP3 usando `yt-dlp`. Pensada para **macOS**: el usuario final la ejecuta con doble clic en archivos `.command`, sin tocar la terminal.

Todo el proyecto está en español: identificadores (`obtener_info`, `descargar_mp3`, `carpeta_destino`), mensajes al usuario (con emojis) y documentación. Mantén esa convención.

## Comandos

No hay tests, linter ni `requirements.txt`. Las dependencias (`yt-dlp`, `certifi`, sin versión fija) las instala `setup.command`.

```bash
# Setup de desarrollo (equivalente a setup.command, sin prompts ni osascript)
python3 -m venv .venv && .venv/bin/pip install yt-dlp certifi

# Ejecutar el script directamente
.venv/bin/python youtube_downloader.py

# Verificación rápida de sintaxis
python3 -m py_compile youtube_downloader.py

# Prueba no interactiva: obtiene info del video y sale con la opción 3
printf '%s\n' 'https://www.youtube.com/watch?v=VIDEO_ID' 3 | .venv/bin/python youtube_downloader.py
```

Fuera de macOS **no ejecutes los `.command`**: usan `read -p` (bloquean esperando Enter) y terminan con `osascript`, que cierra la ventana o sale por completo de Terminal.app.

Requisitos: **Python 3.10+** (el código usa la sintaxis `dict | None`) y **FFmpeg** en el `PATH` (necesario para convertir a MP3 y para unir `bestvideo+bestaudio` en MP4).

## Arquitectura

El flujo cruza tres archivos:

1. **`youtube_downloader.command`** (launcher): hace `cd` a su propio directorio y valida el `.venv` con `.venv/bin/pip --version`. Si falla (no existe, o la carpeta se movió y las rutas absolutas del venv se rompieron), invoca `./setup.command` y vuelve a verificar. Luego activa el venv y corre el script de Python.
2. **`setup.command`**: verifica `python3`, ofrece `brew install ffmpeg` si falta, recrea `.venv` desde cero si está roto e instala/actualiza dependencias. Es idempotente; se puede correr cuantas veces sea necesario.
3. **`youtube_downloader.py`**: flujo lineal basado en `input()` → `obtener_info()` (`extract_info` con `download=False`) → menú MP3/MP4 → `seleccionar_carpeta()` (default `~/Downloads`) → `descargar_mp3()` o `descargar_mp4()`.

Detalles que no son obvios a simple vista:

- **Contrato de exit code** entre Python y el launcher: código `≠ 0` → la ventana queda abierta esperando Enter para que el usuario lea el error; código `0` → `osascript` cierra la ventana. Si un fallo debe quedar visible, el script tiene que terminar con `sys.exit(1)`. Ojo: hoy `descargar_mp3()`/`descargar_mp4()` capturan `DownloadError` y retornan normalmente, así que un fallo de descarga sale con `0` y la ventana se cierra.
- **La lógica de validación del venv está duplicada** en ambos `.command`. Si cambias el criterio de "venv roto", actualiza los dos.
- **`certifi` debe configurarse antes de `import yt_dlp`**: el script asigna `SSL_CERT_FILE` al inicio porque las instalaciones de Python de python.org en macOS no traen certificados raíz.
- **Selección de formato MP4**: las cadenas de `formatos` en `descargar_mp4()` priorizan `mp4` + `m4a` para que FFmpeg solo haga *remux* (sin re-encode), con *fallback* a `best`. El MP3 usa el postprocessor `FFmpegExtractAudio` a 192 kbps. Ambos guardan con la plantilla `%(title)s.%(ext)s`.
- Los `.command` deben conservar el bit de ejecución (`chmod +x`) para que macOS los abra con doble clic.
