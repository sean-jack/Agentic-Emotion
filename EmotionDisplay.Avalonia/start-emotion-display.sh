#!/bin/bash
# Cross-platform script to start the Avalonia EmotionDisplay application
# Works on macOS and Linux

echo "Checking if EmotionDisplay is already running..."

# Check if the process is running (works on macOS and Linux)
if pgrep -f "EmotionDisplay.Avalonia" > /dev/null; then
    echo "EmotionDisplay is already running!"
    exit 0
fi

echo "EmotionDisplay is not running. Starting it now..."

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Navigate to the project directory
cd "$SCRIPT_DIR/EmotionDisplay.Avalonia"

# Start the EmotionDisplay application
dotnet run --project EmotionDisplay.Avalonia.csproj &

echo "EmotionDisplay started successfully!"
sleep 2

exit 0
