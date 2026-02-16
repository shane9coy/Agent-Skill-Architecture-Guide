# KiloCode Skills Guide

A complete guide to skill registration, folder structure, and agent orchestration for KiloCode.

Compiled from Agent Skills Architecture Guide v4.1 — February 2026

---

## Table of Contents

1. [How Skills Work in KiloCode](#01--how-skills-work-in-kilocode)
2. [KiloCode Folder Structure](#02--kilocode-folder-structure)
3. [Mode-Scoped Skills](#03--mode-scoped-skills)
4. [SKILL.md Anatomy & Frontmatter](#04--skillmd-anatomy--frontmatter)
5. [Skill Subdirectory Conventions](#05--skill-subdirectory-conventions)
6. [Precedence & Loading Order](#06--precedence--loading-order)
7. [AGENTS.md vs CLAUDE.md vs SKILL.md](#07--agentsmd-vs-claudemd-vs-skillmd)
8. [Cross-Platform Compatibility](#08--cross-platform-compatibility)
9. [Installing & Managing Skills](#09--installing--managing-skills)
10. [Troubleshooting](#10--troubleshooting)
11. [Quick Start Templates](#11--quick-start-templates)

---

## 01 — How Skills Work in KiloCode

Skills in KiloCode follow the **AgentSkills spec** — on-demand prompt expansion that loads only when triggered. The framework scans skill folders, reads YAML frontmatter (name + description), and builds a compact `<available_skills>` XML list in the system prompt.

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

---

## 02 — KiloCode Folder Structure

### Project-Level Structure

```
your-project/
|-- .kilocode/
|   |-- AGENTS.md                # Project memory (native standard)
|   |-- skills/                  # Generic skills (all modes)
|   |   |-- new-skill/
|   |   |   |-- SKILL.md
|   |   |   |-- scripts/
|   |   |   |   +-- scaffold.py
|   |   |   +-- references/
|   |   |       +-- best_practices.md
|   |   +-- deploy-prod/
|   |       +-- SKILL.md
|   |-- skills-code/             # Code mode only
|   |   |-- linting-rules/
|   |   |   +-- SKILL.md
|   |   +-- typescript-patterns/
|   |       +-- SKILL.md
|   |-- skills-architect/        # Architect mode only
|   |   +-- microservices/
|   |       +-- SKILL.md
|   |-- skills-debug/            # Debug mode only
|   |   +-- error-analysis/
|   |       +-- SKILL.md
|   +-- skills-ask/              # Ask mode only
|       +-- documentation/
           +-- SKILL.md
```

### Global Structure

```
~/.kilocode/                     # Global config
|-- AGENTS.md                    # Global instructions
|-- skills/                      # All modes, all projects
|   +-- my-global-skill/
|       +-- SKILL.md
|-- skills-code/                 # Code mode, all projects
|   +-- typescript-patterns/
|       +-- SKILL.md
|-- skills-architect/            # Architect mode, all projects
|   +-- system-design/
|       +-- SKILL.md
+-- skills-debug/                # Debug mode, all projects
    +-- troubleshooting/
        +-- SKILL.md
```

### Key Files

| File | Purpose | Loaded |
|------|---------|--------|
| `AGENTS.md` | Project memory & conventions | Every session |
| `CLAUDE.md` | Fallback compatibility | If AGENTS.md missing |
| `skills/*/SKILL.md` | Specialized capabilities | On-demand |
| `skills-{mode}/*/SKILL.md` | Mode-specific skills | On-demand (mode-restricted) |

---

## 03 — Mode-Scoped Skills

KiloCode's unique feature: **mode-specific skill directories**. Restrict skills to specific agent modes by placing them in the appropriate folder.

### Available Modes

| Mode | Directory | Purpose |
|------|-----------|---------|
| **code** | `skills-code/` | Coding, implementation, refactoring |
| **architect** | `skills-architect/` | System design, architecture decisions |
| **ask** | `skills-ask/` | Q&A, documentation, explanations |
| **debug** | `skills-debug/` | Troubleshooting, error analysis |
| **orchestrate** | `skills-orchestrate/` | Multi-step workflows, coordination |

### How Mode Scoping Works

```
Generic skills/          → Available in ALL modes
skills-code/             → Only in Code mode
skills-architect/        → Only in Architect mode
skills-debug/            → Only in Debug mode
skills-ask/              → Only in Ask mode
skills-orchestrate/      → Only in Orchestrate mode
```

### Example: Multi-Mode Project

```
.kilocode/
|-- AGENTS.md
|-- skills/                      # Shared across all modes
|   |-- new-skill/               # Skill installer
|   |   +-- SKILL.md
|   +-- deploy-prod/             # Deployment (all modes)
|       +-- SKILL.md
|-- skills-code/                 # Code mode only
|   |-- linting-rules/
|   |   +-- SKILL.md
|   +-- refactoring-patterns/
|       +-- SKILL.md
|-- skills-architect/            # Architect mode only
|   +-- microservices/
|       +-- SKILL.md
+-- skills-debug/                # Debug mode only
    +-- error-analysis/
        +-- SKILL.md
```

---

## 04 — SKILL.md Anatomy & Frontmatter

KiloCode uses the standard AgentSkills spec — same SKILL.md format as Claude Code and Codex.

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
.kilocode/skills/mcp-builder/
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

KiloCode loads skills in priority order (highest to lowest):

| Priority | Location | Scope |
|----------|----------|-------|
| 1 (highest) | `<project>/.kilocode/skills-{mode}/` | This project, this mode only |
| 2 | `<project>/.kilocode/skills/` | This project, all modes |
| 3 | `~/.kilocode/skills-{mode}/` | Global, mode-specific |
| 4 | `~/.kilocode/skills/` | Global, all modes |
| 5 (lowest) | `.claude/skills/` (fallback) | Cross-tool compatibility |

### How It Works

1. **Mode-specific project skills** win over generic project skills
2. **Project skills** win over global skills
3. **Global mode-specific skills** apply when no project equivalent exists
4. **Generic global skills** are the fallback
5. **`.claude/skills/`** is read for compatibility with Claude Code skills

---

## 07 — AGENTS.md vs CLAUDE.md vs SKILL.md

| File | Loaded | Purpose | Best For |
|------|--------|---------|----------|
| `AGENTS.md` | Every session | Persistent memory (native) | Stack, conventions, commands |
| `CLAUDE.md` | Every session | Fallback compatibility | Same as AGENTS.md |
| `skills/*/SKILL.md` | On-demand | Specialized capability | Workflows, integrations |
| `skills-{mode}/*/SKILL.md` | On-demand (mode-restricted) | Mode-specific capability | Mode-appropriate tasks |

### AGENTS.md (Native Standard)

KiloCode's native memory file — also used by Cursor and Windsurf.

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

### CLAUDE.md (Fallback)

KiloCode reads `CLAUDE.md` as a fallback for cross-tool compatibility with Claude Code.

> **Recommendation:** Use `AGENTS.md` as your primary memory file. It's the open standard.

### Decision Flowchart

```
Does the model need this info EVERY time?
    |
    YES --> AGENTS.md (or CLAUDE.md for compatibility)
    |
    NO
    |
    Does it need it SOMETIMES (triggered by task type)?
        |
        YES --> Is it mode-specific?
            |
            YES --> skills-{mode}/my-skill/SKILL.md
            |
            NO --> skills/my-skill/SKILL.md
        |
        NO --> Probably just put it in AGENTS.md
```

---

## 08 — Cross-Platform Compatibility

KiloCode is designed for maximum compatibility:

### What KiloCode Reads

| Source | Support |
|--------|---------|
| `.kilocode/skills/` | ✅ Native |
| `.kilocode/skills-{mode}/` | ✅ Native (unique feature) |
| `~/.kilocode/skills/` | ✅ Native |
| `.claude/skills/` | ✅ Fallback |
| `CLAUDE.md` | ✅ Fallback |

### For Maximum Compatibility

Ship skills in **both** locations to cover all platforms:

```bash
# Copy skills to both folders for maximum compatibility
mkdir -p .kilocode/skills/my-skill
mkdir -p .claude/skills/my-skill
cp -r my-skill/* .kilocode/skills/my-skill/
cp -r my-skill/* .claude/skills/my-skill/
```

### Platform Coverage Matrix

| Location | KiloCode | Claude Code | Codex |
|----------|----------|-------------|-------|
| `.kilocode/skills/` | ✅ Native | ❌ No | ❌ No |
| `.claude/skills/` | ✅ Fallback | ✅ Native | ❌ No |
| `.codex/skills/` | ❌ No | ❌ No | ✅ Native |
| `.agents/skills/` | ❌ No | ❌ No | ✅ Native |

> **Two folders covers three platforms:** `.kilocode/skills/` + `.claude/skills/` = KiloCode + Claude Code covered.

---

## 09 — Installing & Managing Skills

### Via VS Code UI

1. Open VS Code settings
2. Navigate to KiloCode settings
3. Toggle skills on/off without deleting

### Via Command Line (npx)

```bash
# Install from registry
npx skills install <skill-name>

# Install from GitHub
npx skills install github:user/repo
```

### Manual Installation from GitHub

```bash
# Clone the repository
git clone --depth 1 <repo-url> /tmp/skill-clone

# Find the SKILL.md file
SKILL=$(find /tmp/skill-clone -name "SKILL.md" | head -1)
NAME=$(basename "$(dirname "$SKILL")")

# Copy to your project
mkdir -p .kilocode/skills/$NAME
cp -r "$(dirname "$SKILL")"/* .kilocode/skills/$NAME/

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
mkdir -p .kilocode/skills/$NAME
cp -r "$(dirname "$SKILL")"/* .kilocode/skills/$NAME/
```

### Post-Install Validation

```bash
# Verify skill structure
ls -la .kilocode/skills/<skill-name>/

# Check frontmatter
head -10 .kilocode/skills/<skill-name>/SKILL.md

# Test the skill
# Ask KiloCode something matching the skill's description
```

### Disabling Skills (Without Deleting)

In VS Code settings:
1. Open Settings (Cmd/Ctrl + ,)
2. Search for "KiloCode skills"
3. Toggle individual skills on/off

---

## 10 — Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Skill not in list | Flat file: `skills/SKILL.md` | Must be `skills/<name>/SKILL.md` |
| Silently skipped | Unquoted description | Wrap in double quotes |
| Never triggers | Vague description | Add specific trigger keywords |
| Frontmatter ignored | Missing `---` markers | Must start and end with `---` |
| 1 of N loads | YAML special chars in others | Quote ALL descriptions |
| Triggers but fails | Missing referenced files | Check `scripts/` and `references/` exist |
| Too much context | SKILL.md > 500 lines | Move depth to `references/` |
| Mode skill not loading | Wrong mode directory | Use `skills-{mode}/` format |
| Model ignores skill | Trigger info in body | Move 'when to use' to description |

### Diagnostic Commands

```bash
# Find all skills
find .kilocode/skills -name "SKILL.md"
find .kilocode/skills-* -name "SKILL.md" 2>/dev/null

# Dump frontmatter
for f in .kilocode/skills/*/SKILL.md .kilocode/skills-*/*/SKILL.md; do
  [ -f "$f" ] || continue
  echo "=== $f ==="
  sed -n '/^---$/,/^---$/p' "$f"
done

# Find unquoted descriptions
grep -rn "^description:" .kilocode/skills/ | grep -v '"'

# Check skill sizes
wc -l .kilocode/skills/*/SKILL.md | sort -rn | head

# Verify mode directories
ls -la .kilocode/skills-*/
```

### Common Mistakes

1. **Wrong folder depth:** `skills/SKILL.md` won't work. Must be `skills/name/SKILL.md`.

2. **Missing mode prefix:** Mode directories must be `skills-code/`, not `code-skills/`.

3. **Unquoted YAML:** Special characters in descriptions break parsing.
   ```yaml
   # ❌ BAD
   description: Use when [building] APIs
   
   # ✅ GOOD
   description: "Use when [building] APIs"
   ```

4. **Missing AGENTS.md:** KiloCode prefers AGENTS.md but falls back to CLAUDE.md.

---

## 11 — Quick Start Templates

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

### Project Setup Script

```bash
#!/bin/bash
# setup-kilocode.sh

PROJECT_DIR="${1:-.}"

# Create directory structure
mkdir -p "$PROJECT_DIR/.kilocode/skills"
mkdir -p "$PROJECT_DIR/.kilocode/skills-code"
mkdir -p "$PROJECT_DIR/.kilocode/skills-architect"

# Create AGENTS.md if it doesn't exist
if [ ! -f "$PROJECT_DIR/.kilocode/AGENTS.md" ]; then
  cat > "$PROJECT_DIR/.kilocode/AGENTS.md" << 'EOF'
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
  echo "Created .kilocode/AGENTS.md"
fi

echo "KiloCode structure created in $PROJECT_DIR/.kilocode/"
```

---

*KiloCode Skills Guide*  
Based on Agent Skills Architecture Guide v4.1  
KiloCode / VS Code / AgentSkills Spec  
February 2026
