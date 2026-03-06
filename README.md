# Agent Skills Architecture Kit

Up to date (as of 2/27/26) agentic folder protocal and build out guide for OpenClaw, Claude Code, KiloCode, OpenAI Codex, and any AgentSkills-compatible agent. The repo features drag and drop agent folders with 'new-skill' and 'mcp-builder' skills preinstalled to architect any new agent skill or mcp install/creation — ready to use with Claude Code, KiloCode, OpenAI Codex, OpenClaw, and any AgentSkills-compatible agent.
📄 Get the Full Guide
[Download the Agent Skills Architecture Guide (PDF)] — covers folder structure, SKILL.md anatomy, frontmatter reference, OpenClaw vs Claude Code comparison diagrams, [claude, kilo, codex, legacy agent] agent folder diagrams, self-hosted model config (Ollama / LM Studio ), troubleshooting, and more.

> Follow [@shaneswrld_] on X

---
![xpost1](https://github.com/user-attachments/assets/ba19f9d7-55fd-453f-9079-cba46118ed76)

## 🚀 Install

### Option 1: Download and drag (easiest)
> Drop-in `.claude/`, `.kilocode/`, `.codex/`, `.agents/`, and `.agent/` folders with skills, architecture reference, and starter config — ready to use with Claude Code, KiloCode, OpenAI Codex, OpenClaw, and any AgentSkills-compatible agent. 

1. Download this repo as a ZIP (green **Code** button → **Download ZIP**)
2. Unzip it
3. **Drag and drop the folders into your agent folder:**
   - **For Claude Code:** Drag `.claude/` into your project root
   - **For KiloCode:** Drag `.kilocode/` into your project root (or use `.claude/` as fallback)
   - **For OpenAI Codex:** Drag `.codex/` or `.agents/` into your project root
   - **For OpenClaw:** Drag `.agent/` into your project root
   - **For AGENT.MD:** Drag `.agent/AGENT.MD` into your project root (or copy to your existing `.agent/AGENT.md`)
4. Done — your agent now has skills installed and ready to use

#### How to Drag & Drop MCP Skills

To add MCP skills (like the included `mcp-builder` skill) to your agent:

1. **Download this repo as a ZIP** (green **Code** button → **Download ZIP**)
2. **Unzip it** on your computer
3. **Navigate to the agent folder** you want to add MCP skills to:
   - For OpenClaw: `.agent/skills/` folder inside your project
   - For Claude Code: `.claude/skills/` folder inside your project
   - For KiloCode: `.kilocode/skills/` folder inside your project
   - For OpenAI Codex: `.codex/skills/` folder inside your project
4. **Drag and drop the skill folder** (e.g., `new-mcp-builder/` from `.agent/skills/new-mcp-builder/`) into your agent's `skills/` folder
5. **Restart your agent** — the MCP skill will now be available

> **Note:** The `new-mcp-builder` skill is located at:
> - `.agent/skills/new-mcp-builder/` (OpenClaw)
> - `.claude/skills/new-mcp-builder/` (Claude Code)
> - `.kilocode/skills/new-mcp-builder/` (KiloCode)

#### How to Drag & Drop AGENT.MD

To add the AGENT.MD configuration file to your project:

1. **Download this repo as a ZIP** (green **Code** button → **Download ZIP**)
2. **Unzip it** on your computer
3. **Navigate to** `.agent/` folder in the unzipped repo
4. **Drag and drop `AGENT.MD`** into your project's agent folder:
   - For OpenClaw: Drop into your project's `.agent/` folder
   - For existing `.agent/` folder: Merge with your existing AGENT.md or replace
5. **Restart your agent** — the agent configuration is now loaded

> **Tip:** If you already have an AGENT.MD file, you can merge the contents or use the included one as a template/reference.

> **Tip:** If you already have an agent folder (`.claude/`, `.kilocode/`, `.codex/`, `.agents/`, or `.agent/`), you can just drag the `skills/` subfolder into your existing agent folder to add the skills without overwriting your config.

### Option 2: Clone

```bash
git clone https://github.com/shane9coy/agent-skills-kit.git

# OpenClaw:
cp -r agent-skills-kit/.agent/ your-project/.agent/

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
├── .agent/                                # OpenClaw / general agent
│   ├── AGENT.md                          # Agent configuration and memory
│   └── skills/
│       ├── new-skill-builder/
│       │   ├── SKILL.md                   # Skill installer / scaffolder
│       │   └── references/
│       │       ├── Agent-Skills-Architecture-Guide.md
│       │       └── claude-skills-guide.md
│       └── new-mcp-builder/
│           └── SKILL.md                   # MCP builder skill
│
├── .claude/                              # Claude Code
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

| Tool | Agent folder | Skill folder | Memory file |
|------|-------------|-------------|-------------|
| **OpenClaw** | `.agent/` | `.agent/skills/` | `AGENT.md` |
| **Claude Code** | `.claude/` | `.claude/skills/` | `CLAUDE.md` |
| **KiloCode** | `.kilocode/` | `.kilocode/skills/` (also reads `.claude/skills/`) | `AGENTS.md` (reads `CLAUDE.md` as fallback) |
| **OpenAI Codex** | `.codex/` | `.codex/skills/` (also reads `.agents/skills/`) | `AGENTS.md` |
| **OpenCode** | `.opencode/` | `.opencode/skills/` (also reads `.claude/skills/`) | — |
| **Cursor / Windsurf / Cline** | `.claude/` | `.claude/skills/` via openskills | — |
| **Any AgentSkills agent** | `.agents/` | `.agents/skills/` | — |

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
