# SPECTER - Smart Personal Execution Command Technology Enhanced Responder
### Your Personal PC Voice Assistant

---

## HOW TO SET UP

1. Run `INSTALL.bat` first (only once)
2. Run `START_SPECTER.bat` to launch SPECTER
3. Say **"Specter"** to wake him up
4. Give your command!

---

## VOICE COMMANDS

### 📂 Open Apps
- "Specter, open Chrome"
- "Specter, open Notepad"
- "Specter, open Spotify"
- "Specter, open Discord"
- "Specter, open VS Code"
- "Specter, open WhatsApp"
- "Specter, open Calculator"
- "Specter, open File Explorer"

### ❌ Close Apps
- "Specter, close Chrome"
- "Specter, close Spotify"
- "Specter, kill Discord"

### 🔊 Volume
- "Specter, volume up"
- "Specter, volume down"
- "Specter, mute"
- "Specter, set volume to 50"

### 💡 Brightness
- "Specter, set brightness to 70"
- "Specter, increase brightness"
- "Specter, decrease brightness"

### 🔍 Web Search
- "Specter, search for Real Madrid"
- "Specter, search for War Thunder tips"
- "Specter, open YouTube"
- "Specter, open GitHub"

### 🖥️ System
- "Specter, what time is it"
- "Specter, what's today's date"
- "Specter, take a screenshot"
- "Specter, lock my PC"
- "Specter, sleep"
- "Specter, shutdown" (10 second delay)
- "Specter, restart"
- "Specter, cancel shutdown"

### 👋 Exit
- "Specter, goodbye"
- "Specter, exit"

---

## ADDING MORE APPS

Open `specter.py` and find the `APP_MAP` dictionary.
Add your app like this:

```python
"app name": r"C:\full\path\to\app.exe",
```

---

## REQUIREMENTS
- Windows 10/11
- Python 3.8+
- Internet connection (for speech recognition)
- Microphone

---

*Built by Zayed (Rex) — Powered by Python*
