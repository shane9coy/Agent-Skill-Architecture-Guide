# Agent Skills Architecture Kit

#Drag and drop agent folders with 'new-skill' and 'mcp-builder' skills preinstalled to architect any new agent skill or mcp install/creation — ready to use with Claude Code, KiloCode, OpenAI Codex, OpenClaw, and any AgentSkills-compatible agent.
📄 Get the Full Guide
[Download the Agent Skills Architecture Guide (PDF)] — covers folder structure, SKILL.md anatomy, frontmatter reference, OpenClaw vs Claude Code comparison diagrams, [claude, kilo, codex, legacy agent] agent folder diagrams, self-hosted model config (Ollama / LM Studio ), troubleshooting, and more.

> Follow [@shaneswrld_](https://twitter.com/shaneswrld_) and dm "agent skills" to get the PDF download link.

---
![xpost1](https://github.com/user-attachments/assets/ba19f9d7-55fd-453f-9079-cba46118ed76)

## 🚀 Install

### Option 1: Download and drag (easiest)
> Drop-in `.claude/`, `.kilocode/`, `.codex/`, and `.agents/` folders with a skill installer, architecture reference, and starter config — ready to use with Claude Code, KiloCode, OpenAI Codex, OpenClaw, and any AgentSkills-compatible agent. 

1. Download this repo as a ZIP (green **Code** button → **Download ZIP**)
2. Unzip it
3. Drag the `.claude/` folder into your project root
4. If you use KiloCode, also drag `.kilocode/` in
5. If you use OpenAI Codex, drag `.codex/` in (or `.agents/` + `AGENTS.md`)
6. Done — your agent now has the `new-skill` installer and a starter config

### Option 2: Clone

```bash
git clone https://github.com/shane9coy/agent-skills-kit.git

# Claude Code:
cp -r agent-skills-kit/.claude/ your-project/.claude/

# KiloCode:
cp -r agent-skills-kit/.kilocode/ your-project/.kilocode/

# OpenAI Codex:
cp -r agent-skills-kit/.codex/ your-project/.codex/

# Legacy Codex / .agents convention:
cp -r agent-skills-kit/.agents/ your-project/.agents/
cp agent-skills-kit/AGENTS.md your-project/AGENTS.md
```

---

## 📁 What's Inside

```
agent-skills-kit/
├── .claude/                               # Claude Code
│   ├── CLAUDE.md                          # Starter project config
│   └── skills/
│       └── new-skill/
│           ├── SKILL.md                   # Skill installer / scaffolder / validator
│           └── references/
│               └── claude-skills-guide.md # Architecture reference for the agent
│
├── .kilocode/                             # KiloCode
│   ├── AGENTS.md                          # KiloCode project memory (AGENTS.md standard)
│   └── skills/
│       └── new-skill/
│           ├── SKILL.md
│           └── references/
│               └── claude-skills-guide.md
│
├── .codex/                                # OpenAI Codex
│   ├── AGENTS.md                          # Codex project memory
│   └── skills/
│       └── new-skill/
│           ├── SKILL.md
│           └── references/
│               └── claude-skills-guide.md
│
├── .agents/                               # Legacy / generic AgentSkills
│   └── skills/
│       └── new-skill/
│           ├── SKILL.md
│           └── references/
│               └── claude-skills-guide.md
│
├── AGENTS.md                              # Codex project memory (root-level fallback)
├── README.md
└── LICENSE
```

All four folders contain identical skills — use whichever matches your tool. KiloCode also reads `.claude/skills/` as fallback, so Claude + KiloCode users only need `.claude/`. Codex reads `.codex/skills/` natively and falls back to `.agents/skills/`.

---

## 🛠 What `new-skill` Does

Once installed, your agent gets 5 workflows:

| # | Workflow | How to trigger |
|---|---------|---------------|
| 1 | **Create a skill from scratch** | "create a new skill for X" |
| 2 | **Install from GitHub / zip / markdown** | "install this skill: \<url\>" |
| 3 | **Install the MCP Builder skill** | "set up the mcp-builder skill" |
| 4 | **Validate a skill** | "check if my skill is set up correctly" |
| 5 | **Audit entire agent folder** | "scan and fix my .claude/.codex/.kilocode structure" |

---

## 🔀 Compatibility

The [AgentSkills spec](https://github.com/anthropics/skills) is a shared standard. This kit works with:

| Tool | Skill folder | Memory file |
|------|-------------|-------------|
| **Claude Code** | `.claude/skills/` | `CLAUDE.md` |
| **KiloCode** | `.kilocode/skills/` (also reads `.claude/skills/`) | `AGENTS.md` (reads `CLAUDE.md` as fallback) |
| **OpenAI Codex** | `.codex/skills/` (also reads `.agents/skills/`) | `AGENTS.md` |
| **OpenClaw** | `~/.openclaw/skills/` or `<workspace>/skills/` | `AGENTS.md` + `SOUL.md` |
| **OpenCode** | `.opencode/skills/` (also reads `.claude/skills/`) | — |
| **Cursor / Windsurf / Cline** | `.claude/skills/` via openskills | — |
| **Any AgentSkills agent** | `.agents/skills/` | — |

KiloCode also supports **mode-specific skills** — drop skills into `skills-code/`, `skills-architect/`, `skills-debug/`, etc. to scope them to specific agent modes.

---

## 📖 Key Concepts (from the PDF guide)

- **SKILL.md** — the only required file. YAML frontmatter (`name` + `description`) for discovery, markdown body for instructions.
- **Description is the trigger** — the model matches your request against descriptions, not the body. Put all "when to use" info in the description.
- **Progressive disclosure** — frontmatter is always loaded (~24 tokens/skill), body loads on trigger, references/ load on demand, scripts/ execute on demand.
- **Quote your descriptions** — unquoted YAML with special characters silently breaks registration.
- **Keep SKILL.md under 500 lines** — move depth to `references/`.

---

## 🤝 Credits

Compiled by **s.coy**
[@shaneswrld_](https://twitter.com/shaneswrld_) | [github.com/shane9coy](https://github.com/shane9coy)

---

## 📜 License

MIT — use it, fork it, ship it.
