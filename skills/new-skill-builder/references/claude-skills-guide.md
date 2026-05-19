---
name: claude-folder-architect
description: "Guide for structuring, organizing, and managing .claude/ skill folders for Claude Code, OpenClaw, and compatible CLI agents. Use when setting up a new project, restructuring an existing .claude folder, installing skills, or troubleshooting skill registration issues."
---

# .claude Folder Architecture & Skills Guide

> A complete reference for structuring your `.claude/` folder so that skills register correctly across Claude Code, OpenClaw, KiloCode, and any AgentSkills-compatible CLI agent — including self-hosted models via Ollama or LM Studio.

---

## 1. How Skills Actually Work Under the Hood

Skills are **on-demand prompt expansion**, not agents. Here's the lifecycle:

```
1. DISCOVERY   → Framework scans skill folders, reads YAML frontmatter
2. INDEXING    → Builds <available_skills> list from name + description
3. MATCHING    → User request is matched against descriptions
4. INJECTION   → Matched skill's SKILL.md body is injected into context
5. EXECUTION   → Model follows instructions, runs scripts if needed
```

The model never sees your full SKILL.md until it's triggered. Only the `name` and `description` from frontmatter are in the system prompt at all times. This keeps context lean.

---

## 2. Canonical Folder Structure

### Minimal (one skill)

```
your-project/
├── .claude/
│   ├── CLAUDE.md                    # Project memory (always loaded)
│   └── skills/
│       └── my-skill/
│           └── SKILL.md             # Only required file
```

### Full Production Layout

```
your-project/
├── .claude/
│   ├── CLAUDE.md                    # Project conventions, stack, commands
│   ├── settings.json                # Permissions, allowed tools
│   ├── commands/                    # Custom slash commands
│   │   └── review.md
│   └── skills/
│       ├── mcp-builder/
│       │   ├── SKILL.md
│       │   ├── scripts/
│       │   │   └── scaffold.py
│       │   ├── references/
│       │   │   ├── mcp_best_practices.md
│       │   │   ├── python_mcp_server.md
│       │   │   └── node_mcp_server.md
│       │   └── assets/
│       │       └── template.json
│       ├── new-skill/
│       │   ├── SKILL.md
│       │   └── scripts/
│       │       └── install_skill.sh
│       ├── deploy-prod/
│       │   └── SKILL.md
│       ├── code-review/
│       │   └── SKILL.md
│       └── api-conventions/
│           └── SKILL.md
```

### Global Skills (shared across all projects)

```
~/.claude/
├── CLAUDE.md                        # User-level conventions
└── skills/
    ├── my-global-skill/
    │   └── SKILL.md
    └── formatting-standards/
        └── SKILL.md
```

---

## 3. SKILL.md Anatomy

Every SKILL.md has exactly two parts: YAML frontmatter and markdown body.

```markdown
---
name: my-skill-name
description: "Concise trigger description. Use when [specific condition]. Handles [X, Y, Z]."
---

# Skill Title

## Instructions
Step-by-step instructions the model follows when this skill is invoked.

## Examples
Show input/output pairs so the model understands expected behavior.

## Notes
Edge cases, caveats, things to avoid.
```

### Frontmatter Fields Reference

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | YES | Unique ID, becomes `/skill-name` command. Max 64 chars. |
| `description` | YES | **THE trigger mechanism.** Max 200 chars. Model uses this to decide when to load the skill. |
| `license` | No | License info |
| `context` | No | `fork` = run in subagent, `inline` (default) = run in current context |
| `disable-model-invocation` | No | `true` = only user can invoke via `/name`. Use for destructive ops. |
| `user-invocable` | No | `false` = only model can invoke. Use for background knowledge. |
| `allowed-tools` | No | Restrict tools: `Read, Grep, Glob, Bash, Write` |
| `model` | No | Override model for this skill |
| `metadata` | No | Single-line JSON object for extra data |

### Description Writing Rules

The description is THE most important field. It controls whether your skill ever fires.

**DO:**
- Include specific trigger words users would say
- State both WHAT and WHEN
- Be explicit about file types, actions, contexts

**DON'T:**
- Put "when to use" info in the markdown body (body isn't read until AFTER triggering)
- Use special YAML characters without quotes
- Be vague ("Helps with stuff")

```yaml
# BAD - too vague, will rarely trigger
description: Helps with development tasks

# BAD - unquoted special chars, YAML parse fail, skill silently skipped
description: This handles [brackets] and #hashtags

# GOOD - specific, quoted, actionable
description: "Create, scaffold, and configure new MCP servers for Claude Code and OpenClaw. Use when building tool integrations, API wrappers, or service connectors using the Model Context Protocol."
```

---

## 4. Skill Subdirectory Conventions

### `scripts/` — Executable Code

```
scripts/
├── process.py        # Python scripts Claude runs via Bash tool
├── validate.sh       # Shell scripts
└── generate.js       # Node scripts
```

- Claude executes these with `bash` or `python3`
- Reference them in SKILL.md as: `Run the script at {baseDir}/scripts/process.py`
- `{baseDir}` auto-expands to the skill's folder path

### `references/` — Context Documents

```
references/
├── api-docs.md       # Loaded into context when needed
├── schema.md         # Data model reference
└── examples.md       # Extended examples
```

- These are for **progressive disclosure** — Claude reads them only when needed
- Reference in SKILL.md: "For API details, read `{baseDir}/references/api-docs.md`"
- Keeps SKILL.md under 500 lines

### `assets/` — Templates & Static Files

```
assets/
├── template.json     # Output templates
├── config.yaml       # Default configs
└── logo.png          # Binary assets
```

- Used in output generation, not loaded into context
- Claude copies/modifies these as part of task execution

---

## 5. Precedence & Loading Order

Skills from multiple locations can overlap. Higher precedence wins on name conflict:

### Claude Code

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `<project>/.claude/skills/` | Project-only |
| 2 | `~/.claude/skills/` | All projects |
| 3 | Marketplace/bundled plugins | Global |

### OpenClaw

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `<workspace>/skills/` | Per-agent |
| 2 | `~/.openclaw/skills/` | All agents |
| 3 | Bundled skills | Global |
| 4 (lowest) | `skills.load.extraDirs` entries | Configurable |

### Universal Agents (OpenCode, KiloCode, etc.)

Most scan these paths (varies by tool):
- `.claude/skills/*/SKILL.md`
- `.agents/skills/*/SKILL.md`
- `~/.claude/skills/*/SKILL.md`
- `~/.agents/skills/*/SKILL.md`

---

## 6. CLAUDE.md vs SKILL.md vs Agents

| File | Loaded When | Purpose | Best For |
|------|-------------|---------|----------|
| `CLAUDE.md` | Every session start | Persistent project memory | Stack info, conventions, common commands |
| `SKILL.md` | On-demand (triggered) | Specialized capability | Complex workflows, tool integrations |
| `agents/*.md` | When explicitly spawned | Isolated sub-assistant | Long-running or high-risk tasks |
| `commands/*.md` | When user types `/name` | Slash command template | Quick actions, prompt shortcuts |

**Rule of thumb:** If the model needs it every time → `CLAUDE.md`. If it needs it sometimes → skill. If it's dangerous or long-running → agent.

---

## 7. Self-Hosted Model Configuration

Skills are framework-level, not model-level. The same SKILL.md works regardless of which LLM backs the agent. You just need to configure the provider.

### OpenClaw + Ollama (`~/.openclaw/openclaw.json`)

```json
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://127.0.0.1:11434/v1",
        "apiKey": "ollama-local",
        "api": "openai-completions",
        "models": [
          {
            "id": "qwen3:8b",
            "name": "Qwen3 8B",
            "reasoning": false,
            "input": ["text"],
            "cost": { "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0 },
            "contextWindow": 131072,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "ollama/qwen3:8b" },
      "workspace": "/home/you/.openclaw/workspace",
      "compaction": { "mode": "safeguard" },
      "maxConcurrent": 4
    }
  }
}
```

### OpenClaw + LM Studio

```json
{
  "models": {
    "providers": {
      "lmstudio": {
        "baseUrl": "http://127.0.0.1:1234/v1",
        "apiKey": "lm-studio",
        "api": "openai-completions",
        "models": [
          {
            "id": "glm-4.7-flash",
            "name": "GLM 4.7 Flash",
            "reasoning": true,
            "input": ["text"],
            "cost": { "input": 0, "output": 0 },
            "contextWindow": 128000,
            "maxTokens": 8192
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": { "primary": "lmstudio/glm-4.7-flash" }
    }
  }
}
```

### Model Recommendations by VRAM

| VRAM | Recommended Model | Quant |
|------|-------------------|-------|
| < 8 GB | Qwen3 4B Thinking | Q4_K_M |
| 8-16 GB | Qwen3 8B or Mistral 7B | Q4_K_M |
| 24-48 GB | GLM 4.7 Flash (30B) | Q4_K_M |
| 48-80 GB | Qwen3 Coder (80B) | Q4_K_XL |
| 90+ GB | GPT-OSS 120B | Q4_K_M |

**Critical:** Set `contextWindow` high enough. OpenClaw sends ALL context files (CLAUDE.md + skill content + conversation) with each request. 20K is too low for most setups — aim for 32K minimum.

---

## 8. Troubleshooting: Skills Not Registering

### Checklist

1. **Structure correct?** Must be `skills/<name>/SKILL.md` — NOT `skills/SKILL.md`
2. **Frontmatter valid?** Needs both `name:` and `description:` between `---` markers
3. **Description quoted?** Any special chars (`[]`, `#`, `:`, `'`, `"`) require quotes
4. **File named exactly `SKILL.md`?** Case-sensitive on Linux
5. **Under 500 lines?** Move overflow to `references/` subdirectory
6. **Trigger words in description?** Body text is NOT read until after skill is selected
7. **Restarted service?** OpenClaw watches for changes but sometimes needs a gateway restart
8. **YAML single-line only?** OpenClaw's parser doesn't support multi-line frontmatter values

### Quick Diagnostic

```bash
# Check your skill structure
find .claude/skills -name "SKILL.md" -exec echo "Found: {}" \;

# Validate YAML frontmatter (quick check)
for f in .claude/skills/*/SKILL.md; do
  echo "=== $f ==="
  sed -n '/^---$/,/^---$/p' "$f"
  echo ""
done

# Check for unquoted special chars in descriptions
grep -n "^description:" .claude/skills/*/SKILL.md | grep -v '"'
```

---

## 9. Installing the MCP Builder Skill

The uploaded `mcp-builder` skill should be installed as:

```
.claude/skills/mcp-builder/
├── SKILL.md                         # The uploaded file
├── reference/
│   ├── mcp_best_practices.md        # Must fetch/create
│   ├── python_mcp_server.md         # Must fetch/create
│   ├── node_mcp_server.md           # Must fetch/create
│   └── evaluation.md                # Must fetch/create
```

The SKILL.md references these files via `{baseDir}/reference/`. You need to populate the `reference/` folder for full functionality.

---

## 10. Creating Your Own Skills — Quick Template

```markdown
---
name: your-skill-name
description: "What this does and when to trigger it. Be specific about file types, actions, and contexts."
---

# Your Skill Name

## Overview
One paragraph: what this skill does and why it exists.

## Instructions
1. Step one
2. Step two
3. Step three

## Examples

### Example 1: [Scenario Name]
**Input:** "user says this"
**Action:** Do X, then Y, then Z
**Output:** Expected result

### Example 2: [Scenario Name]
**Input:** "user says this other thing"
**Action:** Different workflow
**Output:** Different result

## Error Handling
- If X fails, do Y
- If API returns 429, wait and retry
- If file not found, suggest alternatives

## Notes
- Keep this under 500 lines
- Move reference material to references/ subfolder
- Test with actual prompts before shipping
```
