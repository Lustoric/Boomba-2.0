# 🎶 Boomba Tunes

Boomba Tunes is a sleek, modern music player built using Python's `customtkinter`, `pygame`, and `mutagen`. It lets you browse and play MP3 files from your system, organized by **artist** and **genre**, with a simple user interface and live progress tracking.

---

## 🚀 Features

- 🎧 Play, pause, stop, next/previous track
- 🔍 Search by **artist** or **genre**
- 📂 Auto-scans your Music folder for `.mp3` files
- 📈 Real-time progress bar and time display
- 🔊 Adjustable volume slider
- 🌙 Dark mode UI using CustomTkinter

---

## 🖼️ UI Preview

*(Add a screenshot of the running app here, e.g., `assets/screenshot.png`)*

---

## 🛠️ Requirements

- Python 3.10 or higher
- Required packages:
  ```bash
  pip install customtkinter pygame mutagen

---

## 🧠 How It Works
- `mutagen` Reads MP3 metadata (artist, genre)
- Songs are listed from your `~/Music` folder
- You can search/filter the songs and play them directly from the interface
