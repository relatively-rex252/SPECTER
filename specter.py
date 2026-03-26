"""
SPECTER - Smart Personal Execution Command Technology Enhanced Responder
Personal Voice Assistant for Dell PC
Author: Zayed (Rex)
"""

import speech_recognition as sr
import pyttsx3
import subprocess
import os
import webbrowser
import time
import threading
import json
import sys

# ─────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────
USERNAME = "dell"
WAKE_WORD = "specter"

# Apps you can open by voice — add more as you like!
APP_MAP = {
    "chrome":       r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "firefox":      r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "notepad":      "notepad.exe",
    "calculator":   "calc.exe",
    "file explorer": "explorer.exe",
    "explorer":     "explorer.exe",
    "task manager": "taskmgr.exe",
    "cmd":          "cmd.exe",
    "command prompt": "cmd.exe",
    "vs code":      rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "vscode":       rf"C:\Users\{USERNAME}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
    "spotify":      rf"C:\Users\{USERNAME}\AppData\Roaming\Spotify\Spotify.exe",
    "discord":      rf"C:\Users\{USERNAME}\AppData\Local\Discord\Update.exe --processStart Discord.exe",
    "vlc":          r"C:\Program Files\VideoLAN\VLC\vlc.exe",
    "word":         r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "excel":        r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE",
    "powerpoint":   r"C:\Program Files\Microsoft Office\root\Office16\POWERPNT.EXE",
    "paint":        "mspaint.exe",
    "whatsapp":     rf"C:\Users\{USERNAME}\AppData\Local\WhatsApp\WhatsApp.exe",
    "brave":        rf"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
    "thunder":      r"steam://rungameid/236390",
    "war thunder":  r"steam://rungameid/236390",
    "steam":        rf"D:\Steam\steam.exe",
}

# ─────────────────────────────────────────
#  SPEECH ENGINE SETUP
# ─────────────────────────────────────────
DAVID_VOICE = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_DAVID_11.0"


def speak(text):
    """SPECTER speaks back — fresh engine each time to avoid blocking mic."""
    print(f"[SPECTER] {text}")

    def _speak():
        try:
            e = pyttsx3.init()
            e.setProperty('rate', 165)
            e.setProperty('volume', 0.9)
            e.setProperty('voice', DAVID_VOICE)
            e.say(text)
            e.runAndWait()
            e.stop()
        except Exception as ex:
            print(f"[SPECTER] Speech error: {ex}")
    t = threading.Thread(target=_speak, daemon=True)
    t.start()
    t.join()

# ─────────────────────────────────────────
#  VOLUME CONTROL
# ─────────────────────────────────────────


def set_volume(level):
    """Set volume 0-100 using Windows built-in."""
    try:
        # Uses nircmd if available, otherwise PowerShell
        script = f"$obj = New-Object -com wscript.shell; $obj.SendKeys([char]173)"
        # Better approach via PowerShell
        ps_cmd = f"""
        $volume = {level / 100}
        $obj = New-Object -ComObject WScript.Shell
        Add-Type -TypeDefinition @'
        using System.Runtime.InteropServices;
        [Guid("5CDF2C82-841E-4546-9722-0CF74078229A"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        interface IAudioEndpointVolume {{
            int f(); int g(); int h(); int i();
            int SetMasterVolumeLevelScalar(float fLevel, System.Guid pguidEventContext);
            int j();
            int GetMasterVolumeLevelScalar(out float pfLevel);
        }}
        [Guid("D666063F-1587-4E43-81F1-B948E807363F"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        interface IMMDevice {{ int Activate([MarshalAs(UnmanagedType.LPStruct)] System.Guid iid, int dwClsCtx, IntPtr pActivationParams, [MarshalAs(UnmanagedType.IUnknown)] out object ppInterface); }}
        [Guid("A95664D2-9614-4F35-A746-DE8DB63617E6"), InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
        interface IMMDeviceEnumerator {{ int f(); int GetDefaultAudioEndpoint(int dataFlow, int role, out IMMDevice ppDevice); }}
        [ComImport, Guid("BCDE0395-E52F-467C-8E3D-C4579291692E")] class MMDeviceEnumeratorClass {{}}
'@
        $enumerator = [Activator]::CreateInstance([Type]::GetTypeFromCLSID([Guid]"BCDE0395-E52F-467C-8E3D-C4579291692E"))
        $device = $null
        ([IMMDeviceEnumerator]$enumerator).GetDefaultAudioEndpoint(0, 1, [ref]$device)
        $ep = $null
        $device.Activate([Guid]"5CDF2C82-841E-4546-9722-0CF74078229A", 1, [IntPtr]::Zero, [ref]$ep)
        ([IAudioEndpointVolume]$ep).SetMasterVolumeLevelScalar({level/100}, [Guid]::Empty)
        """
        subprocess.run(["powershell", "-Command", ps_cmd], capture_output=True)
        speak(f"Volume set to {level} percent")
    except Exception as e:
        speak("Sorry, I couldn't adjust the volume")
        print(f"Volume error: {e}")


def volume_up():
    """Press volume up key."""
    subprocess.run(["powershell", "-Command",
                    "(New-Object -ComObject WScript.Shell).SendKeys([char]175)"])
    speak("Volume up")


def volume_down():
    """Press volume down key."""
    subprocess.run(["powershell", "-Command",
                    "(New-Object -ComObject WScript.Shell).SendKeys([char]174)"])
    speak("Volume down")


def mute_volume():
    """Toggle mute."""
    subprocess.run(["powershell", "-Command",
                    "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"])
    speak("Toggled mute")

# ─────────────────────────────────────────
#  BRIGHTNESS CONTROL
# ─────────────────────────────────────────


def set_brightness(level):
    """Set screen brightness 0-100."""
    try:
        ps_cmd = f"(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,{level})"
        result = subprocess.run(
            ["powershell", "-Command", ps_cmd], capture_output=True)
        if result.returncode == 0:
            speak(f"Brightness set to {level} percent")
        else:
            speak("Brightness adjustment may not be supported on your display")
    except Exception as e:
        speak("Couldn't adjust brightness")
        print(f"Brightness error: {e}")

# ─────────────────────────────────────────
#  APP CONTROL
# ─────────────────────────────────────────


def open_app(app_name):
    """Open an application by name."""
    app_name_lower = app_name.lower().strip()

    if app_name_lower in APP_MAP:
        path = APP_MAP[app_name_lower]
        try:
            # Handle steam:// protocol URLs
            if path.startswith("steam://"):
                os.startfile(path)
            else:
                subprocess.Popen(path, shell=True)
            speak(f"Opening {app_name}")
        except Exception as e:
            speak(f"Couldn't open {app_name}. Make sure it's installed.")
            print(f"App error: {e}")
    else:
        # Try to open it directly anyway
        try:
            subprocess.Popen(app_name_lower, shell=True)
            speak(f"Trying to open {app_name}")
        except:
            speak(
                f"I don't know how to open {app_name}. You can add it to my app list in the config.")


def close_app(app_name):
    """Close an application by process name."""
    process_map = {
        "chrome":       "chrome.exe",
        "google chrome": "chrome.exe",
        "firefox":      "firefox.exe",
        "notepad":      "notepad.exe",
        "calculator":   "calculator.exe",
        "vs code":      "Code.exe",
        "vscode":       "Code.exe",
        "spotify":      "Spotify.exe",
        "discord":      "Discord.exe",
        "vlc":          "vlc.exe",
        "word":         "WINWORD.EXE",
        "excel":        "EXCEL.EXE",
        "powerpoint":   "POWERPNT.EXE",
        "whatsapp":     "WhatsApp.exe",
        "brave":        "Brave.exe",

    }

    app_lower = app_name.lower().strip()
    process = process_map.get(app_lower, app_name)

    try:
        subprocess.run(["taskkill", "/f", "/im", process], capture_output=True)
        speak(f"Closing {app_name}")
    except Exception as e:
        speak(f"Couldn't close {app_name}")
        print(f"Close error: {e}")

# ─────────────────────────────────────────
#  WEB SEARCH
# ─────────────────────────────────────────


def search_web(query):
    """Search Google for something."""
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    speak(f"Searching Google for {query}")


def open_website(site):
    """Open a specific website."""
    site_map = {
        "youtube":   "https://youtube.com",
        "google":    "https://google.com",
        "facebook":  "https://facebook.com",
        "twitter":   "https://twitter.com",
        "github":    "https://github.com",
        "reddit":    "https://reddit.com",
        "whatsapp":  "https://web.whatsapp.com",
        "netflix":   "https://netflix.com",
        "real madrid": "https://realmadrid.com",
        "ac milan":  "https://acmilan.com",
    }

    site_lower = site.lower().strip()
    url = site_map.get(site_lower, f"https://{site_lower}.com")
    webbrowser.open(url)
    speak(f"Opening {site}")

# ─────────────────────────────────────────
#  COMMAND PROCESSOR
# ─────────────────────────────────────────


def process_command(command):
    """Parse and execute a voice command."""
    command = command.lower().strip()
    print(f"[CMD] {command}")

    # ── Greetings ──
    if any(w in command for w in ["hello", "hi", "hey", "what's up", "whats up"]):
        speak("Hey! What can I do for you?")

    # ── Open App ──
    elif command.startswith("open "):
        app = command.replace("open ", "").strip()
        open_app(app)

    # ── Close App ──
    elif command.startswith("close ") or command.startswith("kill "):
        app = command.replace("close ", "").replace("kill ", "").strip()
        close_app(app)

    # ── Volume ──
    elif "volume up" in command or "increase volume" in command or "turn up" in command:
        volume_up()
    elif "volume down" in command or "decrease volume" in command or "turn down" in command:
        volume_down()
    elif "mute" in command or "unmute" in command:
        mute_volume()
    elif "set volume" in command or "volume to" in command:
        # Extract number from command
        words = command.split()
        for word in words:
            if word.isdigit():
                level = max(0, min(100, int(word)))
                set_volume(level)
                break

    # ── Brightness ──
    elif "brightness" in command:
        words = command.split()
        for word in words:
            if word.isdigit():
                level = max(0, min(100, int(word)))
                set_brightness(level)
                break
        else:
            if "increase" in command or "up" in command:
                set_brightness(80)
            elif "decrease" in command or "down" in command:
                set_brightness(40)

    # ── Web Search ──
    elif command.startswith("search ") or command.startswith("search for "):
        query = command.replace("search for ", "").replace(
            "search ", "").strip()
        search_web(query)

    elif command.startswith("open ") and any(s in command for s in ["youtube", "google", "facebook", "twitter", "github", "reddit", "netflix"]):
        site = command.replace("open ", "").strip()
        open_website(site)

    # ── System ──
    elif "screenshot" in command:
        speak("Taking a screenshot")
        subprocess.run(["powershell", "-Command",
                        "Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.SendKeys]::SendWait('%{PRTSC}')"])

    elif "shutdown" in command or "shut down" in command:
        speak("Shutting down in 10 seconds. Say cancel to stop.")
        time.sleep(3)
        os.system("shutdown /s /t 10")

    elif "restart" in command:
        speak("Restarting in 10 seconds.")
        os.system("shutdown /r /t 10")

    elif "cancel shutdown" in command or "abort" in command:
        os.system("shutdown /a")
        speak("Shutdown cancelled")

    elif "sleep" in command or "hibernate" in command:
        speak("Putting your PC to sleep")
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

    elif "lock" in command:
        speak("Locking your PC")
        os.system("rundll32.exe user32.dll,LockWorkStation")

    # ── Time / Date ──
    elif "time" in command:
        current_time = time.strftime("%I:%M %p")
        speak(f"It's {current_time}")

    elif "date" in command:
        current_date = time.strftime("%B %d, %Y")
        speak(f"Today is {current_date}")

    # ── Exit ──
    elif any(w in command for w in ["goodbye", "bye", "exit", "quit", "stop", "shut up"]):
        speak("See you later!")
        sys.exit(0)

    else:
        speak("I didn't catch that. Try saying open, close, search, volume, or brightness.")


# ─────────────────────────────────────────
#  WAKE WORD LISTENER (Simple mode)
# ─────────────────────────────────────────
recognizer = sr.Recognizer()
recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True


def listen_for_wake_word():
    """Continuously listen for 'Hey specter'."""
    print("[SPECTER] Listening for wake word: 'Specter'...")
    print("[SPECTER] Tip: Speak clearly and say 'Specter' in one breath.")

    # Wake word variations to catch different pronunciations
    wake_variations = ["specter", "specter",
                       "spector", "spectre", "spec", "specter please"]

    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                recognizer.energy_threshold = 200  # More sensitive
                recognizer.pause_threshold = 0.8

                audio = recognizer.listen(
                    source, timeout=None, phrase_time_limit=5)

            try:
                text = recognizer.recognize_google(audio).lower()
                # Shows everything it hears
                print(f"[SPECTER] Heard: '{text}'")

                if any(w in text for w in wake_variations):
                    print("[SPECTER] Wake word detected!")
                    speak("Yes?")
                    listen_for_command()

            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("[SPECTER] No internet. Retrying in 5 seconds...")
                time.sleep(5)

        except Exception as e:
            print(f"[SPECTER] Error: {e}")
            time.sleep(1)


def listen_for_command():
    """Listen for a command after wake word."""
    with sr.Microphone() as source:
        print("[SPECTER] Listening for command...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print(f"[SPECTER] Heard: {command}")
            process_command(command)
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
        except sr.RequestError:
            speak("Speech service is unavailable. Check your internet.")


# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 45)
    print("  SPECTER - Smart Personal Execution Command Technology Enhanced Responder")
    print("  Say 'Specter' to wake me up!")
    print("=" * 45)
    speak("Hi Boss, Specter here. Say specter to wake me up!")
    listen_for_wake_word()
