# Codex Skills Guide

A complete guide to skill registration, folder structure, and agent orchestration for OpenAI Codex.

Compiled from Agent Skills Architecture Guide v4.1 — February 2026

---

## Table of Contents

1. [How Skills Work in Codex](#01--how-skills-work-in-codex)
2. [Codex Folder Structure](#02--codex-folder-structure)
3. [Upward Directory Scanning](#03--upward-directory-scanning)
4. [SKILL.md Anatomy & Frontmatter](#04--skillmd-anatomy--frontmatter)
5. [Skill Subdirectory Conventions](#05--skill-subdirectory-conventions)
6. [Precedence & Loading Order](#06--precedence--loading-order)
7. [AGENTS.md & Override System](#07--agentsmd--override-system)
8. [Config.toml Reference](#08--configtoml-reference)
9. [Cross-Platform Compatibility](#09--cross-platform-compatibility)
10. [Installing & Managing Skills](#10--installing--managing-skills)
11. [Troubleshooting](#11--troubleshooting)
12. [Quick Start Templates](#12--quick-start-templates)

---

## 01 — How Skills Work in Codex

Skills in Codex follow the **AgentSkills spec** — on-demand prompt expansion that loads only when triggered. The framework scans skill folders, reads YAML frontmatter (name + description), and builds a compact `<available_skills>` XML list in the system prompt.

### The Lifecycle

| Phase | What Happens | Context Cost |
|-------|--------------|--------------|
| 1. Discovery | Framework scans `*/SKILL.md` in skill paths | 0 tokens |
| 2. Indexing | Builds `<available_skills>` from name + description | ~24 tok/skill |
| 3. Matching | User request matched against descriptions | 0 extra |
| 4. Injection | Full SKILL.md body injected into conversation | Varies (body size) |
| 5. Execution | Model follows instructions, runs scripts | Script output tokens |

### Key Principle: Lazy Loading

Skills cost almost nothing until triggered. Only the frontmatter (name + description) sits in the system prompt (~24 tokens per skill). The full body loads on-demand when matched.

### Built-in Skill Installer

Codex includes `$skill-installer` — a built-in tool for installing and managing skills.

---

## 02 — Codex Folder Structure

### Project-Level Structure

Codex supports two folder names: `.codex/` (native, current) and `.agents/` (legacy fallback).

```
your-project/
|-- .codex/                      # Native (current)
|   |-- AGENTS.md                # Project memory
|   |-- AGENTS.override.md       # Override (takes priority)
|   +-- skills/
|       |-- new-skill/
|       |   |-- SKILL.md
|       |   |-- scripts/
|       |   |   +-- install.py
|       |   +-- references/
|       |       +-- best_practices.md
|       +-- deploy-prod/
|           |-- SKILL.md
|           +-- scripts/
|               +-- deploy.sh
|
|-- .agents/                     # Legacy fallback
|   |-- AGENTS.md
|   +-- skills/
|       +-- my-skill/
|           +-- SKILL.md
|
|-- AGENTS.md                    # Root-level project memory
+-- .agents/                     # Alternative location
    +-- skills/
        +-- my-skill/
            +-- SKILL.md
```

### Global Structure

```
~/.codex/                        # Global config
|-- AGENTS.md                    # Global instructions
|-- AGENTS.override.md           # Global override (takes priority)
|-- config.toml                  # Skill enable/disable config
+-- skills/
    |-- .system/                 # Built-in skills (plan, skill-creator)
    |   |-- plan/
    |   |   +-- SKILL.md
    |   +-- skill-creator/
    |       +-- SKILL.md
    +-- my-global-skill/         # Your global skills
        |-- SKILL.md
        |-- scripts/
        +-- references/
```

### Key Files

| File | Purpose | Loaded |
|------|---------|--------|
| `AGENTS.md` | Project memory & conventions | Every session |
| `AGENTS.override.md` | Override base AGENTS.md | Every session (priority) |
| `config.toml` | Skill configuration | Session start |
| `skills/*/SKILL.md` | Specialized capabilities | On-demand |
| `skills/.system/*` | Built-in system skills | On-demand |

---

## 03 — Upward Directory Scanning

Codex has a unique behavior: **it scans UPWARD from your current working directory to the repo root**, checking every directory for skills.

### How It Works

```
/repo-root
  |-- .codex/
  |   +-- skills/          ← Found (if CWD is anywhere below)
  |
  |-- packages/
  |   |-- frontend/
  |   |   |-- .codex/
  |   |   |   +-- skills/  ← Found (if CWD is frontend/ or below)
  |   |   +-- src/
  |   +-- backend/
  |       |-- .codex/
  |       |   +-- skills/  ← Found (if CWD is backend/ or below)
  |       +-- src/
  +-- shared/
      +-- .codex/
          +-- skills/      ← Found (if CWD is shared/ or below)
```

### Practical Implications

1. **Parent directory skills are inherited**
   ```bash
   cd /repo-root/packages/frontend
   # Skills from /repo-root/.codex/skills/ are available
   # Skills from /repo-root/packages/frontend/.codex/skills/ are available
   ```

2. **Monorepo-friendly**
   - Shared skills at repo root
   - Package-specific skills in subdirectories

3. **Override capability**
   - Child directories can override parent skills with same name

### Comparison: Scan Direction

| Platform | Scan Direction | Behavior |
|----------|----------------|----------|
| **Codex** | CWD → root (upward) | Inherits parent skills |
| Claude Code | root → down | Project-only skills |
| KiloCode | root → down | Project-only skills |

---

## 04 — SKILL.md Anatomy & Frontmatter

Codex uses the standard AgentSkills spec — same SKILL.md format as Claude Code and KiloCode.

### Basic Structure

```yaml
---
name: my-skill-name
description: "Concise trigger. Use when [X]. Handles [Y, Z]."
---

# Skill Title

## Instructions
Step-by-step instructions the model follows...

## Examples
Input/output pairs showing expected behavior...

## Error Handling
What to do when things fail...
```

### Frontmatter Reference

| Field | Required | Purpose |
|-------|----------|---------|
| `name` | ✅ YES | Unique ID. Max 64 chars. Becomes `/skill-name` command. |
| `description` | ✅ YES | **THE trigger.** Max 200 chars. Must include WHAT + WHEN. |
| `license` | No | License info string |
| `context` | No | `fork` = subagent, `inline` = current context (default) |
| `disable-model-invocation` | No | `true` = only user can invoke (destructive ops) |
| `user-invocable` | No | `false` = only model can invoke (background knowledge) |
| `allowed-tools` | No | Restrict tools: Read, Grep, Glob, Bash, Write |
| `model` | No | Override model for this skill only |
| `metadata` | No | Single-line JSON. Extra key-value data. |

### Description Best Practices

| Example | Verdict |
|---------|---------|
| `Helps with development tasks` | ❌ Too vague |
| `This handles [brackets] and #tags` | ❌ Unquoted special chars |
| `"Create MCP servers. Use when building API integrations."` | ✅ Specific + quoted |
| `"Deploy to production. Use when pushing releases or shipping."` | ✅ Clear trigger |

> ⚠️ **Critical:** Always wrap descriptions in double quotes. Unquoted YAML special characters cause silent skipping.

---

## 05 — Skill Subdirectory Conventions

| Directory | Contents | How the Model Uses It |
|-----------|----------|----------------------|
| `scripts/` | Python, Bash, JS executables | Runs via Bash tool. Ref: `{baseDir}/scripts/x.py` |
| `references/` | API docs, schemas, guides | Read on-demand via progressive disclosure |
| `assets/` | Templates, configs, images | Copied or modified during output generation |

### Progressive Disclosure

Show the model just enough to decide, then reveal more as needed:

| Layer | What's Exposed | When |
|-------|----------------|------|
| 1. Frontmatter | name + description | Always — every request |
| 2. SKILL.md body | Full instructions + examples | When skill is triggered |
| 3. references/* | Deep docs, schemas, API refs | When SKILL.md says to read them |
| 4. scripts/* | Executable code + output | When instructions call for execution |

> 💡 **Tip:** Keep SKILL.md under 500 lines. Move depth to `references/`.

### Example Skill with Subdirectories

```
.codex/skills/mcp-builder/
|-- SKILL.md                     # Main skill file
|-- scripts/
|   |-- scaffold.py              # Scaffolding script
|   +-- validate.py              # Validation script
|-- references/
|   |-- mcp_best_practices.md    # Deep documentation
|   +-- api_reference.md         # API details
+-- assets/
    |-- template.json            # Starter template
    +-- config.yaml              # Default config
```

---

## 06 — Precedence & Loading Order

Codex loads skills in priority order (highest to lowest):

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `<cwd>/.codex/skills/` or `<cwd>/.agents/skills/` | Current directory |
| 2 | Parent directories (upward scan) | Inherited |
| 3 | `~/.codex/skills/` | Global |
| 4 | `~/.codex/skills/.system/` | Built-in system skills |

### Override Behavior

- **Same-level override:** `AGENTS.override.md` beats `AGENTS.md` at the same level
- **Child override:** Skills in child directories override parent skills with same name
- **Config override:** `config.toml` can disable skills without deleting

---

## 07 — AGENTS.md & Override System

Codex uses `AGENTS.md` for project memory (not `CLAUDE.md`). The override system lets you temporarily change behavior.

### AGENTS.md (Base Memory)

```markdown
# Project Configuration

## Stack
- Language: TypeScript 5.x
- Framework: Next.js 14
- Database: PostgreSQL
- Deployment: Vercel

## Commands
- `npm run dev`    -- Start dev server
- `npm test`       -- Run test suite
- `npm run build`  -- Production build

## Code Conventions
- TypeScript strict mode
- Functional components with hooks
- Tailwind for styling

## Notes
- Run tests before committing
- Conventional commits (feat:, fix:)
```

### AGENTS.override.md (Priority Override)

Create an override file at the same level to temporarily change behavior:

```markdown
# Override Configuration

## Temporary Changes
- Using experimental branch
- Skip tests for now
- Deploy to staging only
```

### Override Resolution

| Location | Priority |
|----------|----------|
| `<cwd>/.codex/AGENTS.override.md` | Highest |
| `<cwd>/.codex/AGENTS.md` | Base |
| `~/.codex/AGENTS.override.md` | Global override |
| `~/.codex/AGENTS.md` | Global base |

### Use Cases for Overrides

1. **Temporary experimentation** without modifying base config
2. **Per-directory customizations** in monorepos
3. **Global preferences** in `~/.codex/AGENTS.override.md`
4. **CI/CD specific settings** via environment-specific overrides

---

## 08 — Config.toml Reference

Codex uses `~/.codex/config.toml` for skill configuration — including the ability to disable skills without deleting them.

### Basic Structure

```toml
# ~/.codex/config.toml

[skills.config]
enabled = true  # Default for all skills

[[skills.config]]
name = "risky-skill"
enabled = false  # Disable this specific skill

[[skills.config]]
name = "experimental-skill"
enabled = false
```

### Configuration Options

| Option | Type | Description |
|--------|------|-------------|
| `skills.config.enabled` | boolean | Default enable state |
| `[[skills.config]].name` | string | Skill name to configure |
| `[[skills.config]].enabled` | boolean | Enable/disable specific skill |

### Disabling Skills Without Deleting

```toml
# Disable a problematic skill
[[skills.config]]
name = "buggy-skill"
enabled = false

# Disable multiple skills
[[skills.config]]
name = "skill-one"
enabled = false

[[skills.config]]
name = "skill-two"
enabled = false
```

### Comparison: Disable Methods

| Platform | Method |
|----------|--------|
| **Codex** | `config.toml` [[skills.config]] |
| Claude Code | Settings UI toggle |
| KiloCode | VS Code settings toggle |

---

## 09 — Cross-Platform Compatibility

### What Codex Reads

| Source | Support |
|--------|---------|
| `.codex/skills/` | ✅ Native |
| `.agents/skills/` | ✅ Legacy fallback |
| `~/.codex/skills/` | ✅ Native |
| `CLAUDE.md` | ❌ No (uses AGENTS.md) |
| `.kilocode/skills/` | ❌ No |

### For Maximum Compatibility

Ship skills in **both** locations to cover all platforms:

```bash
# Copy skills to both folders for maximum compatibility
mkdir -p .codex/skills/my-skill
mkdir -p .agents/skills/my-skill
mkdir -p .claude/skills/my-skill
cp -r my-skill/* .codex/skills/my-skill/
cp -r my-skill/* .agents/skills/my-skill/
cp -r my-skill/* .claude/skills/my-skill/
```

### Platform Coverage Matrix

| Location | Codex | Claude Code | KiloCode |
|----------|-------|-------------|----------|
| `.codex/skills/` | ✅ Native | ❌ No | ❌ No |
| `.agents/skills/` | ✅ Native | ❌ No | ❌ No |
| `.claude/skills/` | ❌ No | ✅ Native | ✅ Fallback |
| `.kilocode/skills/` | ❌ No | ❌ No | ✅ Native |

> **Three folders covers all platforms:** `.codex/skills/` + `.agents/skills/` + `.claude/skills/` = Codex + Claude Code + KiloCode covered.

---

## 10 — Installing & Managing Skills

### Via Built-in Skill Installer

Codex includes `$skill-installer` for managing skills:

```bash
# Install a skill (built-in)
$skill-installer install <skill-name>

# List available skills
$skill-installer list
```

### Manual Installation from GitHub

```bash
# Clone the repository
git clone --depth 1 <repo-url> /tmp/skill-clone

# Find the SKILL.md file
SKILL=$(find /tmp/skill-clone -name "SKILL.md" | head -1)
NAME=$(basename "$(dirname "$SKILL")")

# Copy to your project
mkdir -p .codex/skills/$NAME
cp -r "$(dirname "$SKILL")"/* .codex/skills/$NAME/

# Cleanup
rm -rf /tmp/skill-clone
```

### Manual Installation from Zip

```bash
# Extract the zip
unzip skill.zip -d /tmp/install

# Find the SKILL.md file
SKILL=$(find /tmp/install -name "SKILL.md" | head -1)
NAME=$(grep "^name:" "$SKILL" | sed 's/name: *//' | tr -d '"')

# Copy to your project
mkdir -p .codex/skills/$NAME
cp -r "$(dirname "$SKILL")"/* .codex/skills/$NAME/
```

### Post-Install Validation

```bash
# Verify skill structure
ls -la .codex/skills/<skill-name>/

# Check frontmatter
head -10 .codex/skills/<skill-name>/SKILL.md

# Test the skill
# Ask Codex something matching the skill's description
```

### Disabling Skills (Without Deleting)

Edit `~/.codex/config.toml`:

```toml
[[skills.config]]
name = "skill-to-disable"
enabled = false
```

---

## 11 — Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill not in list | Flat file: `skills/SKILL.md` | Must be `skills/<name>/SKILL.md` |
| Silently skipped | Unquoted description | Wrap in double quotes |
| Never triggers | Vague description | Add specific trigger keywords |
| Frontmatter ignored | Missing `---` markers | Must start and end with `---` |
| 1 of N loads | YAML special chars in others | Quote ALL descriptions |
| Triggers but fails | Missing referenced files | Check `scripts/` and `references/` exist |
| Too much context | SKILL.md > 500 lines | Move depth to `references/` |
| Override not working | Wrong file name | Must be `AGENTS.override.md` |
| Skill won't disable | Wrong config format | Use `[[skills.config]]` in config.toml |
| Model ignores skill | Trigger info in body | Move 'when to use' to description |

### Diagnostic Commands

```bash
# Find all skills (including upward scan)
find .codex/skills ~/.codex/skills -name "SKILL.md" 2>/dev/null

# Dump frontmatter
for f in .codex/skills/*/SKILL.md ~/.codex/skills/*/SKILL.md; do
  [ -f "$f" ] || continue
  echo "=== $f ==="
  sed -n '/^---$/,/^---$/p' "$f"
done

# Find unquoted descriptions
grep -rn "^description:" .codex/skills/ ~/.codex/skills/ 2>/dev/null | grep -v '"'

# Check skill sizes
wc -l .codex/skills/*/SKILL.md ~/.codex/skills/*/SKILL.md 2>/dev/null | sort -rn | head

# Verify config.toml
 cat ~/.codex/config.toml
```

### Common Mistakes

1. **Wrong folder depth:** `skills/SKILL.md` won't work. Must be `skills/name/SKILL.md`.

2. **Using CLAUDE.md:** Codex uses `AGENTS.md`, not `CLAUDE.md`.

3. **Unquoted YAML:** Special characters in descriptions break parsing.
   ```yaml
   # ❌ BAD
   description: Use when [building] APIs
   
   # ✅ GOOD
   description: "Use when [building] APIs"
   ```

4. **Wrong override filename:** Must be `AGENTS.override.md`, not `AGENTS.override`.

5. **Config.toml syntax:** Use double brackets for array tables.
   ```toml
   # ❌ BAD
   [skills.config]
   name = "my-skill"
   enabled = false
   
   # ✅ GOOD
   [[skills.config]]
   name = "my-skill"
   enabled = false
   ```

---

## 12 — Quick Start Templates

### SKILL.md Template

```yaml
---
name: your-skill-name
description: "What it does. Use when [trigger]. Handles [X, Y]."
---

# Your Skill Name

## Overview
One paragraph explaining purpose.

## Instructions
1. First step
2. Second step
3. Third step

## Examples

### Example 1: [Scenario]
**Input:** "user says this"
**Action:** Do X, then Y
**Output:** Expected result

## Error Handling
- If X fails, do Y

## Notes
- Keep under 500 lines
- Move depth to references/
```

### AGENTS.md Template

```markdown
# Project Configuration

## Stack
- Language: [Python 3.12 / TypeScript 5.x]
- Framework: [FastAPI / Next.js]
- Database: [PostgreSQL / SQLite]
- Deployment: [Docker / Vercel]

## Commands
- `npm run dev`    -- Start dev server
- `npm test`       -- Run test suite
- `npm run build`  -- Production build
- `npm run lint`   -- Lint and format

## Code Conventions
- TypeScript strict mode
- Functional components with hooks
- Tailwind for styling
- Tests colocated next to source

## Architecture
- /src/components  -- React components
- /src/lib         -- Shared utilities
- /src/api         -- Route handlers
- /src/types       -- Type definitions

## Notes
- Run tests before committing
- Conventional commits (feat:, fix:)
- Never commit .env files
```

### AGENTS.override.md Template

```markdown
# Override Configuration

## Temporary Changes
- [Add temporary modifications here]
- [These override the base AGENTS.md]

## Notes
- Delete this file to revert to base configuration
- Useful for experimentation and CI/CD
```

### Config.toml Template

```toml
# ~/.codex/config.toml

# Default: enable all skills
[skills.config]
enabled = true

# Disable specific skills
[[skills.config]]
name = "skill-to-disable"
enabled = false
```

### Project Setup Script

```bash
#!/bin/bash
# setup-codex.sh

PROJECT_DIR="${1:-.}"

# Create directory structure
mkdir -p "$PROJECT_DIR/.codex/skills"

# Create AGENTS.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/.codex/AGENTS.md" ]; then
  cat > "$PROJECT_DIR/.codex/AGENTS.md" << 'EOF'
# Project Configuration

## Stack
- Language: 
- Framework: 
- Database: 
- Deployment: 

## Commands
- 

## Code Conventions
- 

## Notes
- 
EOF
  echo "Created .codex/AGENTS.md"
fi

# Create global config if it doesn't exist
if [ ! -f "$HOME/.codex/config.toml" ]; then
  mkdir -p "$HOME/.codex"
  cat > "$HOME/.codex/config.toml" << 'EOF'
[skills.config]
enabled = true
EOF
  echo "Created ~/.codex/config.toml"
fi

echo "Codex structure created in $PROJECT_DIR/.codex/"
```

---

*Codex Skills Guide*  
Based on Agent Skills Architecture Guide v4.1  
OpenAI Codex / AgentSkills Spec  
February 2026
