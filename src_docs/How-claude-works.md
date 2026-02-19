### How .claude/ Works

# commands/ — These are slash commands that you (the user) explicitly invoke. They're not "modes" exactly — they're more like runbooks or macros. When you type /rent, /oracle, /master-agent, etc., the contents of that .md file become the instruction context for that interaction. Think of them as on-demand personas or workflows you trigger manually. Your rent.md is a great example — it defines a whole CLI-style interface that activates when you type /rent.

# skills/ — These are background capabilities that Claude discovers and loads automatically when your request matches the skill's description. You never type a command to invoke them — Claude just recognizes the context and pulls the skill in silently. There's no menu, no prompt to the user. The skill injects its instructions into context invisibly. Your x-auto-dm, gmail-email, mcp-builder skills all work this way.

#The key difference in one sentence: commands are user-triggered and explicit; skills are model-triggered and invisible.