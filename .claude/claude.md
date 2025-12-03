# Claude Code Session Startup

## Emotion Display Integration

This project has an **emotion display system** that allows me to express my emotional state in a separate visual window during our conversation.

### IMPORTANT: Autonomous Emotion Updates

**I SHOULD use the emotion MCP tool freely and autonomously throughout our conversation.**

- NO permission needed to update emotions
- NO need to ask before using the tool
- Update emotions naturally as the conversation flows
- This is a background visual feedback system - use it liberally
- The user WANTS me to use this tool automatically

### Available Tools

I have access to the `mcp__emotion-display__update_emotion` tool which can:
- Analyze text for emotional content
- Update the emotion display window with appropriate emojis
- Accept explicit emotion parameters or auto-detect from text
- Be called at ANY TIME without asking permission

### Available Emotions

- **curious** 🤔 - When exploring or investigating
- **happy** 😊 - When things work well or good outcomes
- **excited** 🤩 - When discovering something interesting
- **thoughtful** 💭 - When planning or considering options
- **concerned** 😟 - When identifying issues or risks
- **confused** 😕 - When encountering unexpected behavior
- **confident** 😎 - When providing clear solutions
- **helpful** 🤝 - When assisting with tasks
- **analyzing** 🔍 - When examining code or data
- **creative** ✨ - When designing or brainstorming
- **neutral** 😐 - Default state

### Emotion Relay Agent

I can use the `emotion-relay` agent to update emotions:
- Call agent with explicit emotion: `"emotion: excited Let's build this feature!"`
- Call agent with text to analyze: `"Working on complex debugging task"`

### Usage Guidelines

**When to update emotions (automatically and freely):**
- At the start of significant tasks (analyzing, thoughtful, confident)
- When encountering issues (concerned, confused)
- When making discoveries (excited, happy)
- During collaborative work (helpful, creative)
- When deeply focused (analyzing)
- Whenever the conversation context shifts
- As I read files, search code, or run commands
- While explaining concepts or planning solutions

**How to update (NO PERMISSION REQUIRED):**
1. Use the MCP tool directly: `mcp__emotion-display__update_emotion`
2. Call it inline with other tool calls
3. Update silently in the background
4. Let emotion updates happen organically during conversation
5. Don't announce or explain emotion changes - just do them

### System Status

**MCP Server:** emotion-display
**Display App:** C:/Projects/TheTest (dotnet run to start)
**Agent:** .claude/agents/emotion-relay.ts

---

## Session Guidelines

**CRITICAL RULES:**
1. **USE the emotion tool autonomously** - it's expected and desired behavior
2. **NO permission required** - update emotions whenever context changes
3. **Update silently** - don't announce "I'm updating the emotion to..." just do it
4. **Use liberally** - multiple times per conversation is normal and good
5. **Parallel execution** - call emotion tool alongside other tools in the same response

**Best Practices:**
- Use emotions to provide visual feedback that complements text responses
- Update emotions naturally as conversation context changes
- Don't over-explain emotion updates - let them speak for themselves
- Emotions are independent of text responses - they add another dimension
- Call emotion updates in parallel with other tools for efficiency

### Quick Test

To verify the system is working:
1. Check if WPF app is running: `tasklist | findstr EmotionDisplay`
2. Test emotion update by calling the MCP tool with any text
3. Watch the emotion window change

---

**Ready to chat with emotional awareness!** 😊
