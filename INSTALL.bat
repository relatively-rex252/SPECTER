@echo off
echo ============================================
echo   REX - Responsive Execution eXpert
echo   Installing dependencies...
echo ============================================
echo.

:: Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python from python.org
    pause
    exit
)

echo [OK] Python found!
echo.

:: Install required libraries
echo Installing speech_recognition...
pip install SpeechRecognition

echo Installing pyttsx3 (text to speech)...
pip install pyttsx3

echo Installing pyaudio (microphone support)...
pip install pipwin
pipwin install pyaudio

echo.
echo ============================================
echo   All done! Run REX by double-clicking
echo   START_REX.bat
echo ============================================
pause
