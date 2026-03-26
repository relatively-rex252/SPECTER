# 👻 SPECTER
### Smart Personal Execution Command Technology Enhanced Responder

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python)
![Platform](https://img.shields.io/badge/Platform-Windows-0078D6?style=for-the-badge&logo=windows)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

> A voice-activated personal AI assistant for Windows — say **"Specter"** and it executes your commands instantly.

---

## 🎯 What is SPECTER?

SPECTER is a lightweight, offline-friendly voice assistant for Windows PCs. No Cortana, no Alexa, no subscriptions — just say the wake word and SPECTER gets to work. Open apps, control your system, search the web, adjust volume and brightness, all by voice.

Built with Python. Runs in the background. Completely yours.

---

## ✨ Features

- 🎙️ **Wake Word Detection** — Just say *"Specter"* to activate
- 📂 **App Control** — Open and close any application by voice
- 🔊 **Volume Control** — Turn up, turn down, mute, or set exact level
- 💡 **Brightness Control** — Adjust screen brightness by voice
- 🔍 **Web Search** — Search Google or open any website hands-free
- 🖥️ **System Commands** — Lock, sleep, shutdown, restart, screenshot
- 🕐 **Time & Date** — Ask SPECTER what time or date it is
- 💬 **Voice Feedback** — SPECTER talks back to you

---

## 🚀 Getting Started

### Requirements
- Windows 10 or 11
- Python 3.8 or higher → [Download Python](https://python.org)
- A working microphone
- Internet connection (for speech recognition)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/relatively-rex252/SPECTER.git
cd SPECTER
```

**2. Install dependencies**

Simply double-click `INSTALL.bat` — it handles everything automatically.

Or manually via pip:
```bash
pip install SpeechRecognition pyttsx3 pyaudio
```

**3. Run SPECTER**

Double-click `START_SPECTER.bat` or run:
```bash
python specter.py
```

---

## 🗣️ Voice Commands

| Category | Command Examples |
|----------|-----------------|
| **Wake** | *"Specter"* |
| **Open Apps** | *"Open Chrome"*, *"Open Spotify"*, *"Open VS Code"* |
| **Close Apps** | *"Close Chrome"*, *"Kill Discord"* |
| **Volume** | *"Volume up"*, *"Volume down"*, *"Mute"*, *"Set volume to 50"* |
| **Brightness** | *"Set brightness to 70"*, *"Increase brightness"* |
| **Web Search** | *"Search for Real Madrid"*, *"Open YouTube"* |
| **System** | *"Lock my PC"*, *"Sleep"*, *"Shutdown"*, *"Take a screenshot"* |
| **Info** | *"What time is it"*, *"What's today's date"* |
| **Exit** | *"Goodbye"*, *"Exit"* |

---

## ⚙️ Adding More Apps

Open `specter.py` and find the `APP_MAP` dictionary. Add your app like this:

```python
APP_MAP = {
    "your app name": r"C:\full\path\to\your\app.exe",
}
```

---

## 🛠️ Built With

- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) — Voice input
- [pyttsx3](https://pypi.org/project/pyttsx3/) — Text to speech (offline)
- [PyAudio](https://pypi.org/project/PyAudio/) — Microphone access
- [subprocess / os](https://docs.python.org/3/library/subprocess.html) — System control

---

## 📁 Project Structure

```
SPECTER/
├── specter.py          # Main assistant script
├── START_SPECTER.bat   # Launch SPECTER
├── INSTALL.bat         # Install dependencies
└── README.md           # You are here
```

---

## 🔮 Roadmap

- [ ] System tray icon
- [ ] Custom wake word training
- [ ] Weather updates by voice
- [ ] WhatsApp / messaging integration
- [ ] GUI dashboard
- [ ] Offline speech recognition

---

## 👤 Author

**Zayed** — [@YOUR_GITHUB](https://github.com/relatively-rex252)

> *"Built because I wanted Bixby, but for my PC."*

---

## 📄 License

This project is licensed under the MIT License — feel free to use, modify, and share it.

---

⭐ If you found SPECTER useful, leave a star on the repo!
