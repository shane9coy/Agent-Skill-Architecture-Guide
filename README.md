# Agent Skills Architecture Guide

Agent-skills guide and starter kit for using `AGENTS.md`, `SKILL.md`, and repo-local agent folders to make AI coding agents behave more predictably inside real codebases.

This repo now focuses on a simplified layout:

- `AGENTS.md`: public template for agent behavior, Git hygiene, contextual editing, implementation review, and handoff discipline.
- `skills/agent-copy/`: reusable skill for copying your canonical global instructions into any project repo and appending repo-specific guidance.
- `skills/new-skill-builder/`: reusable skill for creating, installing, validating, and auditing agent skills.
- `skills/new-mcp-builder/`: reusable skill for planning and building MCP server integrations.
- `Agent-Skills-Architecture-Guide.md`: Markdown source for the guide.
- `Agent-Skills-Architecture-Guide-v2.pdf`: PDF version of the guide.
- `socialmediamockup.txt`: draft social article copy for launch/content work.

📄 Get the Full Guide

[Download the Agent Skills Architecture Guide v2 PDF](Agent-Skills-Architecture-Guide-v2.pdf)

The guide covers agent folder structure, `AGENTS.md`, `SKILL.md` anatomy, frontmatter reference, orchestration folders, command-folder equivalents, self-hosted model notes, troubleshooting, and reusable skill patterns.

> Copy the included `AGENTS.md` into your canonical global agent instruction folder, then replace the placeholder Git identity fields with your own name, email, and GitHub username.

![Agent Skills Architecture Guide cover](assets/title-cover.png)

## Install

### Option 1: Install `AGENTS.md`

Open `AGENTS.md` and replace:

- `<YOUR_GIT_AUTHOR_NAME>`
- `<YOUR_GIT_AUTHOR_EMAIL>`
- `<YOUR_GITHUB_USERNAME>`

Install globally for Codex:

```bash
mkdir -p ~/.codex
cp AGENTS.md ~/.codex/AGENTS.md
```

Install repo-locally:

```bash
cp AGENTS.md your-project/AGENTS.md
```

Global rules define how your agent should behave everywhere. Repo-local rules define how the agent should behave inside one specific codebase.

Codex is the default example in this repo, so the default canonical source is:

```bash
~/.codex/AGENTS.md
```

If your canonical agent instructions live somewhere else, keep the same workflow and change the source path. The model is:

```text
canonical global instructions -> repo-local AGENTS.md -> repo-specific tail
```

### Option 2: Install Skills

Copy the included skills into your agent skill folder:

```bash
mkdir -p ~/.codex/skills
cp -R skills/new-skill-builder ~/.codex/skills/
cp -R skills/new-mcp-builder ~/.codex/skills/
cp -R skills/agent-copy ~/.codex/skills/
```

For repo-local usage, copy the skill folders into your project:

```bash
mkdir -p your-project/skills
cp -R skills/new-skill-builder your-project/skills/
cp -R skills/new-mcp-builder your-project/skills/
cp -R skills/agent-copy your-project/skills/
```

Use your agent's equivalent skill directory if you are using Claude Code, KiloCode, Hermes Agent, OpenCode, Cursor, Windsurf, Cline, or another AgentSkills-compatible agent.

### Option 3: Clone

```bash
git clone https://github.com/shane9coy/Agent-Skill-Architecture-Guide.git
cd Agent-Skill-Architecture-Guide
```

Then install `AGENTS.md` and the skills using the commands above.

## Recommended Workflow

1. Install `AGENTS.md` globally so every agent session starts with the same operating rules.
2. Install `agent-copy` so your agent can create repo-local `AGENTS.md` files without manual copy/paste.
3. Run `agent-copy` inside each important repo so local sessions have a reliable fallback.
4. Add repo-specific guidance underneath the global rules: stack, commands, branch rules, build/test flow, project boundaries, and known risks.
5. Install `new-skill-builder` when you want your agent to create or validate skills.
6. Install `new-mcp-builder` when you want your agent to plan or build MCP integrations.

After installing `agent-copy`, open a target project and ask your agent:

```text
Use agent-copy to create or refresh this repo's AGENTS.md from my canonical global instructions, then add repo-specific guidance based on the files in this project.
```

If your canonical source is not `~/.codex/AGENTS.md`, provide the exact source path:

```text
Use agent-copy with SOURCE_AGENTS=/path/to/my/global/instructions.md to create or refresh this repo's AGENTS.md, then add repo-specific guidance based on the files in this project.
```

## What's Inside

```text
Agent-Skill-Architecture-Guide/
├── AGENTS.md
├── Agent-Skills-Architecture-Guide.md
├── Agent-Skills-Architecture-Guide-v2.pdf
├── README.md
├── LICENSE
├── socialmediamockup.txt
└── skills/
    ├── agent-copy/
    │   └── SKILL.md
    ├── new-mcp-builder/
    │   ├── SKILL.md
    │   └── references/
    └── new-skill-builder/
        ├── SKILL.md
        └── references/
```

## What The Skills Do

### `agent-copy`

Use this skill when you want an agent to:

- Copy your canonical global instructions into the current repo's `AGENTS.md`.
- Preserve the canonical rules exactly.
- Add repo-specific guidance based on the current codebase.
- Keep future repo-local `AGENTS.md` files aligned with your global operating rules.
- Use Codex's `~/.codex/AGENTS.md` by default, while allowing another canonical source path when needed.

### `new-skill-builder`

Use this skill when you want an agent to:

- Create a new skill from scratch.
- Install a skill from GitHub, ZIP, or Markdown.
- Validate a skill's structure and frontmatter.
- Audit an agent skill folder.
- Move long reference material out of `SKILL.md` and into `references/`.

### `new-mcp-builder`

Use this skill when you want an agent to:

- Plan a new MCP server.
- Define tool surfaces and schemas.
- Document setup, auth, environment variables, and safety boundaries.
- Create implementation notes for MCP integrations.
- Review an MCP server for usability and agent compatibility.

## Compatibility

This repo uses the shared AgentSkills pattern:

| Tool | Suggested instruction file | Suggested skill folder |
|------|----------------------------|------------------------|
| OpenAI Codex | `AGENTS.md` | `.codex/skills/`, `.agents/skills/`, or repo `skills/` |
| Hermes Agent | `AGENTS.md` or context files | Hermes skills path or repo `skills/` |
| KiloCode | `AGENTS.md` | `.kilocode/skills/` |
| Claude Code | `CLAUDE.md` / project instructions | `.claude/skills/` |
| OpenCode | tool-specific context | `.opencode/skills/` |
| Cursor / Windsurf / Cline | tool-specific context | compatible imported skills folder |
| Any AgentSkills agent | tool-specific context | repo `skills/` |

## Key Concepts

- **`AGENTS.md`**: Durable agent instructions for behavior, Git hygiene, contextual editing, stack conventions, verification, and handoff expectations.
- **`SKILL.md`**: Skill entrypoint with YAML frontmatter for discovery and Markdown body for instructions.
- **`references/`**: Supporting material loaded only when needed.
- **Progressive disclosure**: Keep the core skill short and move deeper examples or guides into references.
- **Description is the trigger**: The model matches the request against skill descriptions, so put "when to use" guidance in the description.

## Credits

Compiled by [@shaneswrld_](https://github.com/shane9coy)

## License

MIT — use it, fork it, ship it. All I ask for is credit where credit is due.
