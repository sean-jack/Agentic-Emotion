# EmotionDisplay.Avalonia - Cross-Platform Edition

A cross-platform emotion display application built with Avalonia UI. Runs on Windows, macOS, and Linux.

## What's New

This is a cross-platform version of the original WPF EmotionDisplay app. Key differences:

- **Cross-platform support**: Windows, macOS, and Linux
- **Avalonia UI framework**: Modern, cross-platform XAML framework
- **Same functionality**: All 11 emotions, named pipe communication, MCP integration
- **Native look**: Adapts to each platform's UI conventions

## Quick Start

### Windows

```batch
cd EmotionDisplay.Avalonia
dotnet run --project EmotionDisplay.Avalonia.csproj
```

### macOS / Linux

```bash
cd EmotionDisplay.Avalonia
./start-emotion-display.sh
```

Or manually:
```bash
cd EmotionDisplay.Avalonia
dotnet run --project EmotionDisplay.Avalonia.csproj
```

## Prerequisites

- **.NET 8 SDK** or higher (Avalonia uses .NET 9 by default)
- Supported on:
  - **Windows** 10/11 (x64, x86, ARM64)
  - **macOS** 10.15+ (x64, ARM64/Apple Silicon)
  - **Linux** with X11 or Wayland

## Installation

1. **Install .NET SDK**:
   - Windows/macOS/Linux: https://dotnet.microsoft.com/download

2. **Clone the repository**:
   ```bash
   git clone https://github.com/sean-jack/Agentic-Emotion.git
   cd Agentic-Emotion/EmotionDisplay.Avalonia
   ```

3. **Build the project**:
   ```bash
   cd EmotionDisplay.Avalonia
   dotnet build
   ```

4. **Run the app**:
   ```bash
   dotnet run
   ```

## Communication Protocol

The app uses **named pipes** (Windows) or **Unix domain sockets** (macOS/Linux) for IPC:

- **Windows**: Named pipe at `\\.\pipe\EmotionDisplayPipe`
- **macOS/Linux**: Unix socket at `/tmp/EmotionDisplayPipe`

### Sending Emotions

Use the cross-platform Python client:

```python
from display_client_crossplatform import send_emotion

send_emotion("happy")  # Works on all platforms
```

## Available Emotions

- `curious` 🤔
- `happy` 😊
- `excited` 🤩
- `thoughtful` 💭
- `concerned` 😟
- `confused` 😕
- `confident` 😎
- `helpful` 🤝
- `analyzing` 🔍
- `creative` ✨
- `neutral` 😐 (default)

## Helper Scripts

### macOS / Linux

- **Start app**: `./start-emotion-display.sh`
- **Check status**: `./check-emotion-display.sh`

### Windows

Use the batch scripts in the parent directory:
- **Start app**: `..\start-emotion-display.bat`
- **Check status**: `..\check-emotion-display.bat`

## MCP Integration

The Avalonia version works with the same MCP emotion server as the WPF version. No changes needed to your Claude Code configuration.

## Platform-Specific Notes

### Windows
- Uses native Windows named pipes
- Same behavior as the original WPF version
- Window style: Tool window with border decorations

### macOS
- Uses Unix domain sockets in `/tmp`
- Native macOS window chrome
- Supports both Intel and Apple Silicon

### Linux
- Requires X11 or Wayland display server
- Uses Unix domain sockets
- Tested on Ubuntu, Fedora, Arch

## Troubleshooting

### App Won't Start

**Check .NET version:**
```bash
dotnet --version
```
Should be 8.0 or higher.

**Build first:**
```bash
dotnet build
```

### Emotions Not Updating

**Check if app is running:**
- macOS/Linux: `pgrep -f EmotionDisplay.Avalonia`
- Windows: `tasklist | findstr EmotionDisplay`

**Test the communication:**
```bash
cd ../mcp-emotion-server
python display_client_crossplatform.py
```

### Linux-Specific Issues

**Missing dependencies:**
```bash
# Ubuntu/Debian
sudo apt install libx11-dev libice-dev libsm-dev

# Fedora
sudo dnf install libX11-devel libICE-devel libSM-devel
```

## Architecture

```
Python MCP Server
    ↓
platform-specific IPC
    ↓ (named pipe on Windows, Unix socket on macOS/Linux)
Avalonia App (.NET)
    ↓
Native UI (WPF on Windows, Cocoa on macOS, GTK/X11 on Linux)
```

## Performance

- **Startup time**: ~1-2 seconds
- **Memory usage**: ~50-80MB
- **CPU usage**: <1% idle, <5% when updating

## Comparison with WPF Version

| Feature | WPF | Avalonia |
|---------|-----|----------|
| Windows | ✅ | ✅ |
| macOS | ❌ | ✅ |
| Linux | ❌ | ✅ |
| UI Framework | WPF | Avalonia |
| Target | .NET 8 | .NET 9 |
| File Size | ~150KB | ~300KB |
| Startup | ~500ms | ~1s |

## Development

### Project Structure

```
EmotionDisplay.Avalonia/
├── EmotionDisplay.Avalonia/
│   ├── App.axaml              # Application entry
│   ├── MainWindow.axaml       # UI layout
│   ├── MainWindow.axaml.cs    # Logic + named pipe server
│   └── EmotionDisplay.Avalonia.csproj
├── start-emotion-display.sh   # macOS/Linux startup
├── check-emotion-display.sh   # Status check
└── README.md                  # This file
```

### Building for Release

```bash
# Windows x64
dotnet publish -c Release -r win-x64 --self-contained

# macOS ARM64 (Apple Silicon)
dotnet publish -c Release -r osx-arm64 --self-contained

# macOS x64 (Intel)
dotnet publish -c Release -r osx-x64 --self-contained

# Linux x64
dotnet publish -c Release -r linux-x64 --self-contained
```

## Migration from WPF

If you're currently using the WPF version:

1. The Avalonia version can run **alongside** the WPF version
2. They use the **same named pipe name** (EmotionDisplayPipe)
3. **Don't run both simultaneously** - they'll conflict on the pipe
4. The MCP server works with **either version** without changes

## License

Part of the Agentic-Emotion project.

## Links

- **Main Project**: https://github.com/sean-jack/Agentic-Emotion
- **Avalonia Docs**: https://docs.avaloniaui.net/
- **Report Issues**: https://github.com/sean-jack/Agentic-Emotion/issues
