# Claude Code Project Notes

## Quick Reference

This directory contains Claude Code configuration and project context for the MCP Emotion Display project.

## Current Working Notes

**Primary Documentation:** `C:/Projects/TheTest/SETUP_NOTES.md`

## Project Overview

MCP-based emotion display system that shows Claude's emotional state in a separate WPF window during conversations.

## Components

1. **WPF Emotion Display App** - .NET app showing emoji-based emotions
2. **Python MCP Server** - Analyzes text and sends emotions via named pipe
3. **MCP Configuration** - Connects Claude to the emotion display

## MCP Server Configuration

### Claude Desktop (Working ✅)
- Config: `%APPDATA%/Claude/claude_desktop_config.json`
- Status: Configured and working

### Claude Code CLI (In Progress ⚙️)
- Config: `~/.claude/mcp_config.json`
- Status: Just configured, needs CLI restart to test
- Path format: Updated to use forward slashes for Git Bash compatibility

## Last Session Status

**Date:** 2025-12-03

**What we did:**
1. User restarted Claude Code CLI after adding MCP config
2. MCP server not showing up in `/mcp` command
3. Identified path format issue (backslashes vs forward slashes)
4. Updated `~/.claude/mcp_config.json` to use forward slashes
5. **Next step:** Restart Claude Code CLI to load the MCP server

**MCP Config Location:** `~/.claude/mcp_config.json`

**Config content:**
```json
{
  "mcpServers": {
    "emotion-display": {
      "command": "python",
      "args": [
        "C:/Projects/TheTest/mcp-emotion-server/server.py"
      ],
      "env": {
        "EMOTION_PIPE_NAME": "EmotionDisplayPipe"
      }
    }
  }
}
```

## After Restart

When you restart Claude Code CLI and come back:

1. Run `/mcp` to verify the server loaded
2. Start the WPF app: `cd C:/Projects/TheTest && dotnet run`
3. Test the emotion display by chatting with Claude
4. Check `SETUP_NOTES.md` for detailed testing instructions

## Files to Reference

- `SETUP_NOTES.md` - Main setup documentation and testing guide
- `mcp-emotion-server/README.md` - MCP server documentation
- `.claude/README.md` - This file (quick context for Claude)

## Environment

- OS: Windows (Git Bash)
- Python: 3.14.0
- Project: C:/Projects/TheTest
- User config: ~/.claude/

## Known Issues

- Claude Code CLI requires restart after MCP config changes
- Path format must use forward slashes in Git Bash environment
- First run downloads AI model (~250MB, one-time)
