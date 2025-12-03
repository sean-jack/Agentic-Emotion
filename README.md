# Emotion Display System

A .NET WPF application that displays visual emotion feedback in a small window, with MCP server integration for AI-powered emotion analysis during Claude Code conversations.

## Quick Start

### Option 1: Using Batch Scripts (Recommended)

1. **Start the EmotionDisplay app:**
   ```batch
   start-emotion-display.bat
   ```
   This will check if EmotionDisplay is already running and start it if needed.

2. **Check if it's running:**
   ```batch
   check-emotion-display.bat
   ```

### Option 2: Manual Start

```bash
dotnet run --project EmotionDisplay.csproj
```

## Components

1. **EmotionDisplay** - WPF app that shows an emoji in a small window
2. **EmotionAgent** - .NET agent with keyword-based emotion analysis
3. **TestAgent** - Console app to test the .NET system
4. **MCP Emotion Server** - Python MCP server for AI-powered analysis with Claude Code
5. **Batch Scripts** - Helper scripts for easy startup

## Available Emotions

- Curious 🤔
- Happy 😊
- Excited 🤩
- Thoughtful 💭
- Concerned 😟
- Confused 😕
- Confident 😎
- Helpful 🤝
- Analyzing 🔍
- Creative ✨
- Neutral 😐 (default)

## Setup Instructions

### Prerequisites

- **.NET 8 SDK** or higher
- **Python 3.9+** (for MCP server integration)
- **Windows OS** (for named pipe support)

### Step 1: Install .NET Dependencies

The EmotionDisplay app uses WPF and .NET 8. Ensure you have the .NET SDK installed:

```bash
dotnet --version
```

If not installed, download from [dotnet.microsoft.com](https://dotnet.microsoft.com/).

### Step 2: Install Python MCP Server (For Claude Code Integration)

1. **Install Python dependencies:**
   ```bash
   cd mcp-emotion-server
   pip install -r requirements.txt
   ```

   This installs:
   - `mcp` - MCP SDK
   - `pywin32` - Windows API for named pipes
   - `transformers` - AI emotion analysis model
   - `torch` - Deep learning framework

2. **Configure Claude Desktop:**

   Edit `%APPDATA%\Claude\claude_desktop_config.json` and add:

   ```json
   {
     "mcpServers": {
       "emotion-display": {
         "command": "python",
         "args": ["C:\\Projects\\TheTest\\mcp-emotion-server\\server.py"],
         "env": {"EMOTION_PIPE_NAME": "EmotionDisplayPipe"}
       }
     }
   }
   ```

   **Important:** Replace `C:\\Projects\\TheTest` with your actual project path. Use double backslashes on Windows.

3. **Restart Claude Desktop** completely (don't just close the window - quit from the system tray).

### Step 3: Start the EmotionDisplay App

Use one of these methods:

**Method 1: Batch script (easiest)**
```batch
start-emotion-display.bat
```

**Method 2: Direct command**
```bash
dotnet run --project EmotionDisplay.csproj
```

You should see a small window with a neutral emoji (😐).

## How It Works

### Architecture

```
Claude Code (conversation)
    ↓ calls MCP tool
Python MCP Server (server.py)
    ↓ analyzes text with AI model
emotion_analyzer.py
    ↓ sends emotion via named pipe
display_client.py
    ↓
.NET WPF App → Updates emoji display
```

### Process Flow

1. The WPF app starts and creates a named pipe server (`EmotionDisplayPipe`)
2. Claude Code analyzes the conversation context
3. Claude calls the MCP `update_emotion` tool autonomously
4. The Python MCP server analyzes text using AI + keywords
5. The emotion is sent through the named pipe
6. The WPF UI updates to show the corresponding emoji

## Usage

### With Claude Code

Once configured, the system works automatically:

1. Start the EmotionDisplay app using `start-emotion-display.bat`
2. Open Claude Code or Claude Desktop
3. During conversation, Claude will autonomously update emotions based on context
4. Watch the emotion window change in real-time

The emotion display provides visual feedback showing Claude's "emotional state":
- 🤔 Curious - When exploring or investigating
- ✨ Creative - When designing or building features
- 🔍 Analyzing - When examining code or data
- 😟 Concerned - When encountering errors or issues
- 😊 Happy - When things work well
- And more!

### Testing the .NET Agent Directly

Run the test console app:

```bash
dotnet run --project TestAgent.csproj
```

Or integrate `EmotionAgent.cs` into your own application:

```csharp
// Analyze a request
string emotion = EmotionAgent.AnalyzeRequest("How do I build this feature?");

// Send to display
EmotionAgent.SendEmotion(emotion);
```

### Manual Testing

**Test the named pipe client:**
```bash
cd mcp-emotion-server
python display_client.py
```

**Test the emotion analyzer:**
```bash
cd mcp-emotion-server
python emotion_analyzer.py
```

## Troubleshooting

### EmotionDisplay Not Starting

**Check if .NET is installed:**
```bash
dotnet --version
```

**Build the project first:**
```bash
dotnet build EmotionDisplay.csproj
```

### EmotionDisplay Already Running

Use the check script:
```batch
check-emotion-display.bat
```

If you need to restart it, close the window and run `start-emotion-display.bat` again.

### MCP Server Not Working

**Check Claude Desktop logs:**
- Location: `%APPDATA%\Claude\logs\`
- Look for MCP server initialization errors

**Verify Python path:**
```bash
where python
```
Make sure this matches the path in your `claude_desktop_config.json`.

**Is the WPF app running?**
```batch
check-emotion-display.bat
```

### Display Not Updating

**Test the named pipe directly:**
```bash
cd mcp-emotion-server
python display_client.py
```

If this fails, ensure:
- The WPF app is running
- The pipe name is correct (`EmotionDisplayPipe`)
- No firewall or antivirus blocking the connection

### AI Model Loading Fails

The server will automatically fall back to keyword-based analysis if the AI model fails to load. Check Python console output for errors.

To force keyword-only mode, edit `mcp-emotion-server\server.py` line 18:
```python
analyzer = EmotionAnalyzer(use_model=False)
```

## Batch Scripts Reference

### `start-emotion-display.bat`
Starts the EmotionDisplay app if it's not already running. Safe to run multiple times.

```batch
start-emotion-display.bat
```

### `check-emotion-display.bat`
Checks if EmotionDisplay is currently running and displays the status.

```batch
check-emotion-display.bat
```

## Advanced Configuration

### Customizing Emotions

Edit `mcp-emotion-server\emotion_analyzer.py` to customize keyword-to-emotion mappings.

### Using Different AI Models

Replace the model in `emotion_analyzer.py` line 27:
```python
model="j-hartmann/emotion-english-distilroberta-base"
```

Any HuggingFace emotion classification model will work.

### Environment Variables

- `EMOTION_PIPE_NAME` - Named pipe name (default: "EmotionDisplayPipe")
- `LOG_LEVEL` - Logging verbosity (default: "INFO")

## Performance

- **Model load time:** 2-5 seconds (one-time on startup)
- **Emotion analysis:** 50-100ms per request
- **Named pipe send:** <10ms
- **Total latency:** ~60-110ms (real-time)

## Documentation

- [MCP Server Details](mcp-emotion-server/README.md) - Comprehensive MCP server documentation
- [Setup Notes](SETUP_NOTES.md) - Development setup notes
- [Claude Instructions](.claude/CLAUDE.md) - Instructions for Claude Code integration

## Project Structure

```
TheTest/
├── EmotionDisplay.csproj      # WPF app project
├── MainWindow.xaml            # UI layout
├── MainWindow.xaml.cs         # UI logic + named pipe server
├── EmotionAgent.cs            # .NET emotion analyzer
├── TestAgent.cs               # Test console app
├── TestAgent.csproj           # Test project
├── start-emotion-display.bat  # Start script
├── check-emotion-display.bat  # Status check script
├── mcp-emotion-server/        # Python MCP server
│   ├── server.py              # MCP entry point
│   ├── emotion_analyzer.py    # AI analysis
│   ├── display_client.py      # Named pipe client
│   └── requirements.txt       # Python deps
└── .claude/                   # Claude Code configuration
    ├── CLAUDE.md              # Claude instructions
    └── agents/                # Custom agents
```

## License

Part of the EmotionDisplay project.
