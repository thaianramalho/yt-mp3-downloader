import subprocess
import os
import sys
import tkinter as tk
from tkinter import simpledialog, messagebox

base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

yt_dlp = os.path.join(base_path, "yt-dlp.exe")
ffmpeg_path = os.path.join(base_path, "ffmpeg", "bin")

output_dir = os.path.join(base_path, "Music", "%(playlist_title)s", "%(title)s.%(ext)s")

os.makedirs(os.path.dirname(output_dir), exist_ok=True)

root = tk.Tk()
root.withdraw()
url = simpledialog.askstring("YouTube MP3", "Cole o link do vídeo ou playlist:")

if url:
    try:
        subprocess.run([
            yt_dlp,
            "-x", "--audio-format", "mp3",
            "--ffmpeg-location", ffmpeg_path,
            "-o", output_dir,
            url
        ], check=True)
        messagebox.showinfo("Sucesso", "Download concluído com sucesso!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Erro", "Ocorreu um erro durante o download.")
else:
    messagebox.showwarning("Cancelado", "Nenhum link foi informado.")
