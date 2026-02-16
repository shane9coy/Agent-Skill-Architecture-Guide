# Agent Skills Kit — Project Config (Codex)

## Skills

This project includes the `new-skill` installer skill. Use it to:

1. **Create a skill from scratch** — "create a new skill for X"
2. **Install from GitHub / zip / markdown** — "install this skill: <url>"
3. **Install the MCP Builder skill** — "set up the mcp-builder skill"
4. **Validate a skill** — "check if my skill is set up correctly"
5. **Audit entire .codex folder** — "scan and fix my .codex structure"

## Skill Folder Convention

Skills live in `.codex/skills/<skill-name>/SKILL.md`. Codex scans upward from CWD to repo root, checking every directory for skills.

Each skill folder may also contain:

- `references/` — architecture docs, guides, examples the agent loads on demand
- `scripts/` — executable code the agent can run
- `assets/` — templates, resources

## Notes

- SKILL.md frontmatter (`name` + `description`) is required for discovery
- Description is the trigger — put all "when to use" info there
- Keep SKILL.md under 500 lines; move depth to `references/`
- Quote YAML descriptions to avoid silent parse failures
- Use `config.toml` [[skills.config]] to disable skills without deleting
- `AGENTS.override.md` at same level takes priority over `AGENTS.md`
