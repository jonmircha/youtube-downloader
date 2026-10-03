#!/usr/bin/env python3
"""
YouTube Downloader
==================
Descarga videos de YouTube en formato MP4 o solo el audio en MP3.

Requisitos:
    pip install "yt-dlp[default,deno]"

Uso:
    python youtube_downloader.py
"""
import os
import sys

# Configurar certificados SSL utilizando certifi (necesario en macOS)
try:
    import certifi
    os.environ['SSL_CERT_FILE'] = certifi.where()
except ImportError:
    pass

import yt_dlp


def obtener_info(url: str) -> dict | None:
    """Obtiene la información del video sin descargarlo."""
    opciones = {"quiet": True}
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            info = ydl.extract_info(url, download=False)
            return info
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error al obtener información del video: {e}")
        return None


CARPETA_DEFAULT = os.path.expanduser("~/Downloads")


def descargar_mp3(url: str, carpeta_destino: str = CARPETA_DEFAULT) -> bool:
    """Descarga solo el audio del video en formato MP3. Devuelve True si tuvo éxito."""
    opciones = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(carpeta_destino, "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": False,
    }

    print("\n🎵 Descargando audio en MP3...")
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("\n✅ Audio descargado correctamente.")
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error al descargar el audio: {e}")
        return False


def descargar_mp4(url: str, carpeta_destino: str = CARPETA_DEFAULT, calidad: str = "best") -> bool:
    """Descarga el video en formato MP4. Devuelve True si tuvo éxito."""
    formatos = {
        "1": "bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "2": "bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "3": "bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
        "4": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    }

    print("\n📺 Selecciona la calidad del video:")
    print("  1) 1080p (Full HD)")
    print("  2) 720p  (HD)")
    print("  3) 480p  (SD)")
    print("  4) Máxima calidad disponible")

    opcion = input("\nElige una opción [1-4] (por defecto 1): ").strip() or "1"
    if opcion not in formatos:
        print("⚠️  Opción no válida. Se usará 1080p por defecto.")
        opcion = "1"

    opciones = {
        "format": formatos[opcion],
        "outtmpl": os.path.join(carpeta_destino, "%(title)s.%(ext)s"),
        "merge_output_format": "mp4",
        "quiet": False,
    }

    print("\n📥 Descargando video en MP4...")
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        print("\n✅ Video descargado correctamente.")
        return True
    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error al descargar el video: {e}")
        return False


def seleccionar_carpeta() -> str:
    """Permite al usuario elegir la carpeta de destino (por defecto Downloads)."""
    carpeta = input(
        f"\n📁 Carpeta de destino (presiona Enter para usar '{CARPETA_DEFAULT}'): "
    ).strip()

    if not carpeta:
        carpeta = CARPETA_DEFAULT
    elif not os.path.exists(carpeta):
        crear = input(f"La carpeta '{carpeta}' no existe. ¿Crearla? [s/n]: ").strip().lower()
        if crear == "s":
            os.makedirs(carpeta, exist_ok=True)
            print(f"✅ Carpeta '{carpeta}' creada.")
        else:
            print(f"⚠️  Se usará la carpeta por defecto ({CARPETA_DEFAULT}).")
            carpeta = CARPETA_DEFAULT

    return carpeta


def main() -> None:
    print("=" * 50)
    print("       🎬  YouTube Downloader con yt-dlp")
    print("=" * 50)

    # Solicitar URL
    url = input("\n🔗 Ingresa la URL del video de YouTube: ").strip()
    if not url:
        print("❌ No ingresaste ninguna URL. Saliendo...")
        sys.exit(1)

    # Mostrar información del video
    print("\n🔍 Obteniendo información del video...")
    info = obtener_info(url)
    if info is None:
        sys.exit(1)

    print(f"\n📌 Título   : {info.get('title', 'Desconocido')}")
    print(f"⏱️  Duración : {info.get('duration_string', 'N/A')}")
    print(f"👤 Canal    : {info.get('uploader', 'N/A')}")
    print(f"👁️  Vistas   : {info.get('view_count') or 0:,}")

    # Seleccionar formato
    print("\n🎛️  ¿Qué deseas descargar?")
    print("  1) 🎵 Solo audio (MP3)")
    print("  2) 🎬 Video completo (MP4)")
    print("  3) ❌ Salir")

    opcion = input("\nElige una opción [1-3]: ").strip()

    # Un exit code distinto de 0 hace que el launcher deje la ventana abierta para leer el error
    if opcion == "1":
        carpeta = seleccionar_carpeta()
        if not descargar_mp3(url, carpeta):
            sys.exit(1)
    elif opcion == "2":
        carpeta = seleccionar_carpeta()
        if not descargar_mp4(url, carpeta):
            sys.exit(1)
    elif opcion == "3":
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    else:
        print("\n⚠️  Opción no válida. Saliendo...")
        sys.exit(1)


if __name__ == "__main__":
    main()
