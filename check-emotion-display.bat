@echo off
REM Batch script to check if EmotionDisplay is running

echo Checking EmotionDisplay status...

REM Check if EmotionDisplay.exe is running
tasklist /FI "IMAGENAME eq EmotionDisplay.exe" 2>NUL | find /I /N "EmotionDisplay.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo [OK] EmotionDisplay is running
    exit /b 0
) else (
    echo [NOT RUNNING] EmotionDisplay is not running
    echo.
    echo To start it, run: start-emotion-display.bat
    exit /b 1
)
