# Agent Skills Architecture Guide Instructions

Shane is the product owner, technical operator, and admin for this project.

This repository is a documentation-first guide for using modern AI coding agents, with a Codex-first emphasis. Keep the writing direct, practical, and mechanism-first. Treat the audience as technically capable but not necessarily familiar with every Codex, skill, or orchestration convention.

## Engineering And Writing Standards

- Start stack-first and architecture-first for substantial changes.
- Preserve the distinction between repo instructions, skills, playbooks, prompts, and task-specific chat context.
- Prefer concrete folder structures, templates, and operational rules over abstract agent theory.
- Do not invent external policies, credentials, production data, or unsupported platform behavior.
- When comparing Claude and Codex, present Claude as a useful reference pattern and Codex as the primary target.
- Keep examples reusable and vendor-aware, but do not make the guide generic when a Codex-specific mechanism is clearer.

## Documentation Shape

- `README.md` is the main paper and overview.
- `.agent/` contains project-local orchestration examples.
- `skills/` contains example Codex skill packages that readers can adapt.
- `templates/` contains copyable scaffolds.

## Change Bar

Every change should make the guide more usable for someone trying to set up agent workflows in a real repo. Avoid bloated taxonomies, vague role names, or command lists that do not explain when and why to use them.
