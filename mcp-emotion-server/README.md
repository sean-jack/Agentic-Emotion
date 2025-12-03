# MCP Emotion Display Server

An MCP server that enables Claude Code to analyze text and update the emotion display window in real-time during conversations.

## Architecture

```
Claude Code (conversation)
    ↓ calls MCP tool
Python MCP Server (server.py)
    ↓ analyzes text
emotion_analyzer.py (AI model + keywords)
    ↓ sends emotion
display_client.py (named pipe)
    ↓
.NET WPF App → Updates emoji display
```

## Features

- **AI-powered emotion detection** using DistilRoBERTa model
- **Keyword fallback** for reliability
- **Real-time updates** to WPF display window
- **11 emotion types**: curious, happy, excited, thoughtful, concerned, confused, confident, helpful, analyzing, creative, neutral
- **Windows named pipe** integration with existing .NET app

## Installation

### Prerequisites

- Python 3.9 or higher
- Windows OS (for named pipe support)
- .NET 8 (for the WPF display app)

### Setup

1. **Install Python dependencies:**

```bash
cd C:\Projects\TheTest\mcp-emotion-server
pip install -r requirements.txt
```

This will install:
- `mcp` - MCP SDK
- `pywin32` - Windows API (named pipes)
- `transformers` - AI model
- `torch` - Deep learning framework

2. **Configure Claude Desktop:**

Edit `%APPDATA%\Claude\claude_desktop_config.json` and add:

```json
{
  "mcpServers": {
    "emotion-display": {
      "command": "python",
      "args": [
        "C:\\Projects\\TheTest\\mcp-emotion-server\\server.py"
      ],
      "env": {
        "EMOTION_PIPE_NAME": "EmotionDisplayPipe"
      }
    }
  }
}
```

**Important:** Use absolute paths and double backslashes on Windows.

3. **Restart Claude Desktop** completely (don't just close the window).

## Usage

### Running the Emotion Display App

First, start the WPF display app:

```bash
cd C:\Projects\TheTest
dotnet run --project EmotionDisplay.csproj
```

You should see a small window with an emoji.

### Using with Claude Code

Once configured, the MCP server runs automatically when you use Claude Desktop. During conversations, Claude can call the `update_emotion` tool to analyze text and update the display.

The tool will be invoked automatically based on conversation context, showing emotions like:
- 🤔 Curious - When asking questions
- ✨ Creative - When building something
- 🔍 Analyzing - When investigating code
- 😟 Concerned - When encountering errors
- 😊 Happy - When things work well

### Testing Components

**Test the named pipe client:**

```bash
python display_client.py
```

This will send test emotions to the display window.

**Test the emotion analyzer:**

```bash
python emotion_analyzer.py
```

This will analyze sample texts and show emotion detection results.

## Configuration

### Environment Variables

- `EMOTION_PIPE_NAME` - Named pipe name (default: "EmotionDisplayPipe")
- `LOG_LEVEL` - Logging verbosity (default: "INFO")

### Emotion Mappings

The analyzer maps text to 11 emotions using:

1. **Context rules** (highest priority):
   - Questions → curious
   - Creation keywords → creative
   - Analysis keywords → analyzing
   - Help requests → helpful

2. **AI model** (6 basic emotions):
   - joy → happy
   - surprise → excited
   - anger/fear → concerned
   - sadness → thoughtful
   - disgust → confused
   - neutral → confident

3. **Keyword fallback** (sentiment-based):
   - Positive words → excited
   - Error/bug words → concerned
   - Uncertainty → thoughtful

## Troubleshooting

### MCP Server Not Loading

**Check Claude Desktop logs:**
- Windows: `%APPDATA%\Claude\logs\`
- Look for MCP server initialization errors

**Verify Python path:**
```bash
where python
```

Make sure the path in `claude_desktop_config.json` matches.

### Display Not Updating

**Is the WPF app running?**
```bash
tasklist | findstr EmotionDisplay
```

**Test the named pipe directly:**
```bash
python display_client.py
```

If this fails, the WPF app isn't running or the pipe name is wrong.

### Model Loading Fails

The server will automatically fall back to keyword-based analysis if the AI model fails to load. Check stderr logs for details.

To force keyword-only mode, edit `server.py` line 18:
```python
analyzer = EmotionAnalyzer(use_model=False)
```

## Performance

- **Model load time:** 2-5 seconds (one-time on startup)
- **Emotion analysis:** 50-100ms per request
- **Named pipe send:** <10ms
- **Total latency:** ~60-110ms (real-time)

## File Structure

```
mcp-emotion-server/
├── server.py              # MCP server entry point
├── emotion_analyzer.py    # AI model + keyword analysis
├── display_client.py      # Named pipe client
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Advanced Usage

### Manual Tool Invocation

You can ask Claude directly:

> "Update the emotion display to show 'excited'"

> "Analyze this text and update the emotion: 'I found a bug'"

### Custom Emotion Mappings

Edit `emotion_analyzer.py` to customize the keyword-to-emotion mappings or adjust the context rules.

### Using Different AI Models

Replace the model in `emotion_analyzer.py` line 27:
```python
model="j-hartmann/emotion-english-distilroberta-base"
```

Any HuggingFace emotion classification model will work.

## Integration with Other Apps

The MCP server works with any application that can act as an MCP client. The `update_emotion` tool can be called from:

- Claude Code (this use case)
- Custom MCP clients
- Other AI tools supporting MCP

## License

Part of the EmotionDisplay project.
