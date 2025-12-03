#!/bin/bash
# Cross-platform script to check if EmotionDisplay is running
# Works on macOS and Linux

echo "Checking EmotionDisplay status..."

# Check if the process is running
if pgrep -f "EmotionDisplay.Avalonia" > /dev/null; then
    echo "[OK] EmotionDisplay is running"
    exit 0
else
    echo "[NOT RUNNING] EmotionDisplay is not running"
    echo ""
    echo "To start it, run: ./start-emotion-display.sh"
    exit 1
fi
