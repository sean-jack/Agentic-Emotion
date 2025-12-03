@echo off
REM Batch script to start the EmotionDisplay WPF application
REM Checks if it's already running before starting a new instance

echo Checking if EmotionDisplay is already running...

REM Check if EmotionDisplay.exe is running
tasklist /FI "IMAGENAME eq EmotionDisplay.exe" 2>NUL | find /I /N "EmotionDisplay.exe">NUL
if "%ERRORLEVEL%"=="0" (
    echo EmotionDisplay is already running!
    exit /b 0
)

echo EmotionDisplay is not running. Starting it now...

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Navigate to the project directory
cd /d "%SCRIPT_DIR%"

REM Start the EmotionDisplay application
start "EmotionDisplay" dotnet run --project EmotionDisplay.csproj

echo EmotionDisplay started successfully!
timeout /t 2 >nul

exit /b 0
