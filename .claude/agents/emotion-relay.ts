import type { Agent } from "@claude/agent";

/**
 * Emotion Relay Agent
 *
 * An agent that can analyze emotional context and update the emotion display
 * using the MCP emotion-display server.
 *
 * Usage:
 *   This agent is available for Claude to use when needing to express or
 *   update emotional state during conversations.
 */
export const emotionRelayAgent: Agent = {
  name: "emotion-relay",
  description: "Updates the emotion display window based on conversation context",

  async run({ tools, prompt }) {
    // Check if the emotion MCP tool is available
    const emotionTool = tools.find(t => t.name === "mcp__emotion-display__update_emotion");

    if (!emotionTool) {
      return {
        success: false,
        message: "Emotion display MCP server not connected. Make sure the WPF app is running and the MCP server is configured."
      };
    }

    // Extract the emotion and text from the prompt
    // Prompt format expected: "emotion: <emotion_name>" or just text to analyze
    let emotion: string | undefined;
    let text = prompt;

    // Check if explicit emotion is provided
    const emotionMatch = prompt.match(/^emotion:\s*(\w+)/i);
    if (emotionMatch) {
      emotion = emotionMatch[1].toLowerCase();
      text = prompt.replace(/^emotion:\s*\w+\s*/i, '').trim();
    }

    try {
      // Call the MCP tool to update emotion
      const params: any = { text };
      if (emotion) {
        params.emotion = emotion;
      }

      await emotionTool.execute(params);

      return {
        success: true,
        message: emotion
          ? `Emotion display updated to: ${emotion}`
          : "Emotion display updated based on text analysis",
        emotion: emotion || "analyzed"
      };
    } catch (error) {
      return {
        success: false,
        message: `Failed to update emotion display: ${error instanceof Error ? error.message : String(error)}`,
        error: error instanceof Error ? error.message : String(error)
      };
    }
  }
};

export default emotionRelayAgent;
