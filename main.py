import customtkinter as ctk
import fnmatch
import os
import time
from pygame import mixer
from mutagen.mp3 import MP3

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("BOOMBA TUNES")
app.geometry("800x600")

mixer.init()
rootpath = "C:\\Users\\yasin\\Music"
pattern = "*.mp3"
currentSongLength = 0
currentSongStartTime = 0

selectedIndex = 0
songs = []

def loadSongs():
    global songs
    for root, dirs, files in os.walk(rootpath):
        for filename in fnmatch.filter(files, pattern):
            songs.append(filename)
    if songs:
        playlistBox.configure(state="normal")
        playlistBox.delete("0.0", "end")
        for song in songs:
            playlistBox.insert("end", song + "\n")
        playlistBox.configure(state="disabled")

def select(index=None):
    global currentSongLength, currentSongStartTime, selectedIndex
    if index is not None:
        selectedIndex = index
    song = songs[selectedIndex]
    songLabel.configure(text=song)
    path = os.path.join(rootpath, song)
    mixer.music.load(path)
    mixer.music.play()
    audio = MP3(path)
    currentSongLength = audio.info.length
    currentSongStartTime = time.time()
    updateProgressBar()

def stop():
    mixer.music.stop()
    progressBar.set(0)
    timeLabel.configure(text="00:00 / 00:00")

def playNext():
    global selectedIndex
    selectedIndex = (selectedIndex + 1) % len(songs)
    highlightSong(selectedIndex)
    select()

def playPrev():
    global selectedIndex
    selectedIndex = (selectedIndex - 1) % len(songs)
    highlightSong(selectedIndex)
    select()

def pauseSong():
    if pauseButton.cget("text") == "Pause":
        mixer.music.pause()
        pauseButton.configure(text="Play")
    else:
        mixer.music.unpause()
        pauseButton.configure(text="Pause")

def setVolume(val):
    mixer.music.set_volume(float(val))

def updateProgressBar():
    if mixer.music.get_busy():
        elapsed = time.time() - currentSongStartTime
        elapsedStr = time.strftime('%M:%S', time.gmtime(elapsed))
        totalStr = time.strftime('%M:%S', time.gmtime(currentSongLength))
        progressBar.set(elapsed / currentSongLength)
        timeLabel.configure(text=f"{elapsedStr} / {totalStr}")
        app.after(1000, updateProgressBar)
    else:
        progressBar.set(0)

def getClickedLine(event):
    line = int(event.y / 20)  # approximate line height
    if 0 <= line < len(songs):
        highlightSong(line)
        select(line)

def highlightSong(index):
    global selectedIndex
    selectedIndex = index
    playlistBox.configure(state="normal")
    playlistBox.delete("0.0", "end")
    for i, song in enumerate(songs):
        if i == index:
            playlistBox.insert("end", f"> {song}\n")
        else:
            playlistBox.insert("end", f"  {song}\n")
    playlistBox.configure(state="disabled")

songLabel = ctk.CTkLabel(app, text="Select a Song", text_color="white", font=("Segoe UI", 20, "bold"))
songLabel.pack(pady=10)

playlistBox = ctk.CTkTextbox(app, height=150, width=700, font=("Segoe UI", 14))
playlistBox.pack(pady=10)
playlistBox.bind("<Button-1>", getClickedLine)
playlistBox.configure(state="disabled")

btnFrame = ctk.CTkFrame(app, fg_color="transparent")
btnFrame.pack(pady=15)

prevButton = ctk.CTkButton(btnFrame, text="⏮ Prev", command=playPrev, width=80)
stopButton = ctk.CTkButton(btnFrame, text="⏹ Stop", command=stop, width=80)
playButton = ctk.CTkButton(btnFrame, text="▶ Play", command=lambda: select(selectedIndex), width=80)
pauseButton = ctk.CTkButton(btnFrame, text="Pause", command=pauseSong, width=80)
nextButton = ctk.CTkButton(btnFrame, text="⏭ Next", command=playNext, width=80)

prevButton.grid(row=0, column=0, padx=5)
stopButton.grid(row=0, column=1, padx=5)
playButton.grid(row=0, column=2, padx=5)
pauseButton.grid(row=0, column=3, padx=5)
nextButton.grid(row=0, column=4, padx=5)

volumeLabel = ctk.CTkLabel(app, text="Volume", font=("Segoe UI", 14))
volumeLabel.pack(pady=(20, 5))

volumeSlider = ctk.CTkSlider(app, from_=0, to=1, command=setVolume)
volumeSlider.set(0.5)
volumeSlider.pack(padx=20, pady=5)

timeLabel = ctk.CTkLabel(app, text="00:00 / 00:00", font=("Segoe UI", 12))
timeLabel.pack(pady=(10, 0))

progressBar = ctk.CTkProgressBar(app, width=600)
progressBar.set(0)
progressBar.pack(pady=(5, 20))

loadSongs()
highlightSong(0)

app.mainloop()
