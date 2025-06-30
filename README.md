# AlyTube 🎬 - YouTube Video & Audio Downloader (Python GUI)

**AlyTube** is a simple, clean, and powerful YouTube video/audio downloader built with Python. It lets you easily download videos in your preferred quality (144p to 1080p+) or extract audio as MP3 — all through a modern, user-friendly GUI. No coding knowledge needed!

![AlyTube Screenshot](screenshot.png) <!-- Optional if you add a screenshot -->

---

## 🚀 Features

- ✅ Download YouTube videos in HD (144p to 1080p+)
- ✅ Supports audio-only (MP3) extraction
- ✅ Playlist support (first video fetch for now)
- ✅ Quality selection dropdown
- ✅ GUI built with `tkinter` (easy to use)
- ✅ Progress bar with percentage
- ✅ Convert to `.exe` for non-technical users
- ✅ Automatic merging of video + audio using `ffmpeg`

---

## 🖥 Tech Stack

- `Python 3.x`
- `yt-dlp`
- `tkinter` GUI
- `ffmpeg` (for merging HD video/audio)
- `pyinstaller` (for EXE conversion)

---

## 📦 Installation

### 🔧 Requirements

- Python 3.8 or higher
- [ffmpeg](https://ffmpeg.org/download.html) (add to PATH)

### 📥 Install dependencies

```bash
pip install yt-dlp
