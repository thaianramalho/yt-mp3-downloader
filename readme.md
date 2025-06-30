# 🎧 YouTube MP3 Downloader GUI (with yt-dlp)

A lightweight and straightforward graphical interface to download YouTube videos or playlists as MP3 files using `yt-dlp` and `ffmpeg`.

This was a personal project, built to avoid bloated third-party apps full of ads, limits, or unnecessary features.

---

## 🧩 Features

- Download individual YouTube videos or entire playlists as MP3
- You can select the audio quality
- Organizes files into folders named after the playlist
- Runs fully offline with local `yt-dlp` and `ffmpeg` (no global installs required)
- Clean GUI with a simple input field for the URL

---

## 📁 Folder Structure

```
YouTubeDownloader/
├── gui.py       # Gui
├── yt-dlp.exe           # yt-dlp binary
├── ffmpeg/
│   └── bin/
│       ├── ffmpeg.exe
│       ├── ffprobe.exe
│       └── ...
```

---

## 🚀 How to Use

1. Download or clone this repository
2. Place `yt-dlp.exe` in the project root
3. Download and extract `ffmpeg`, placing it inside `ffmpeg\bin\`
4. Run `gui.py`
5. Paste a YouTube video or playlist link
6. Click OK — the download and conversion will start automatically

The final MP3 files will be saved where you have selected.

---

## ⚠️ Legal Notice

This project uses `yt-dlp` and `ffmpeg`, powerful tools that access third-party content.
You are responsible for complying with **YouTube’s Terms of Service** and respecting **copyright laws**.
This tool is for **educational and personal use only** — do not use it for redistribution or piracy.

---

## 🛠️ Built With

- Python 3
- yt-dlp
- ffmpeg
- PyInstaller
- tkinter (for the GUI)
