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

# Find dotnet - check common locations
DOTNET_PATH=""
if command -v dotnet &> /dev/null; then
    DOTNET_PATH="dotnet"
elif [ -f "/usr/local/share/dotnet/dotnet" ]; then
    DOTNET_PATH="/usr/local/share/dotnet/dotnet"
elif [ -f "/usr/local/bin/dotnet" ]; then
    DOTNET_PATH="/usr/local/bin/dotnet"
elif [ -f "$HOME/.dotnet/dotnet" ]; then
    DOTNET_PATH="$HOME/.dotnet/dotnet"
fi

if [ -z "$DOTNET_PATH" ]; then
    echo "Error: dotnet command not found. Please install .NET SDK."
    exit 1
fi

# Start the EmotionDisplay application
"$DOTNET_PATH" run --project EmotionDisplay.Avalonia.csproj &

echo "EmotionDisplay started successfully!"
sleep 2

exit 0
