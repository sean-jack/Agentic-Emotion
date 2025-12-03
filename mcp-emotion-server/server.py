#!/usr/bin/env python3
"""
MCP Server for Emotion Display Integration.

This server provides a tool that Claude Code can call to analyze text
and update the emotion display window in real-time.
"""
import sys
import asyncio
from typing import Optional
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

from emotion_analyzer import EmotionAnalyzer
from display_client import send_emotion


# Initialize components
print("Initializing MCP Emotion Display Server...", file=sys.stderr)
analyzer = EmotionAnalyzer(use_model=True)
server = Server("emotion-display")

VALID_EMOTIONS = [
    "curious", "happy", "excited", "thoughtful", "concerned",
    "confused", "confident", "helpful", "analyzing", "creative", "neutral"
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="update_emotion",
            description="Analyze text and update the emotion display window. "
                       "Use this to show visual feedback about the conversation's emotional tone. "
                       "The display shows emojis representing different emotions.",
            inputSchema={
                "type": "object",
                "properties": {
                    "text": {
                        "type": "string",
                        "description": "Text to analyze for emotional content"
                    },
                    "emotion": {
                        "type": "string",
                        "enum": VALID_EMOTIONS,
                        "description": "Explicit emotion to display (optional, skips analysis)"
                    }
                },
                "required": ["text"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Handle tool calls from Claude."""
    if name != "update_emotion":
        raise ValueError(f"Unknown tool: {name}")

    text = arguments.get("text", "")
    explicit_emotion = arguments.get("emotion")

    print(f"Tool called: text='{text[:50]}...', emotion={explicit_emotion}", file=sys.stderr)

    # Determine emotion
    if explicit_emotion and explicit_emotion in VALID_EMOTIONS:
        emotion = explicit_emotion
        print(f"  Using explicit emotion: {emotion}", file=sys.stderr)
    else:
        emotion = analyzer.analyze(text)
        print(f"  Analyzed emotion: {emotion}", file=sys.stderr)

    # Send to display
    success = send_emotion(emotion)

    # Return result
    if success:
        return [
            TextContent(
                type="text",
                text=f"✓ Updated emotion display to '{emotion}'"
            )
        ]
    else:
        return [
            TextContent(
                type="text",
                text=f"✗ Failed to update display (is the EmotionDisplay app running?). "
                     f"Detected emotion was '{emotion}'"
            )
        ]


async def main():
    """Run the MCP server."""
    print("Starting MCP server on stdio...", file=sys.stderr)
    print("Ready to receive requests from Claude Desktop", file=sys.stderr)

    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nShutting down MCP server...", file=sys.stderr)
    except Exception as e:
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(1)
