# Codex Orchestration Model

## Purpose

This file defines the default workflow for coordinating Codex, skills, and specialized agent roles in this project.

## Default Route

1. Read `AGENTS.md`.
2. Read the relevant section of `README.md`.
3. Identify whether the task is documentation, skill design, template creation, review, or implementation.
4. Select the matching playbook from `.agent/playbooks/`.
5. Load or reference any matching skill from `skills/` or `~/.codex/skills/`.
6. Execute the smallest useful slice.
7. Run the review gate.
8. Return a concise handoff.

## Architecture Gate

Before substantial implementation, identify:

- runtime,
- framework,
- data layer,
- service boundaries,
- integrations,
- deployment shape,
- operational constraints.

For this repository, most changes are documentation-only. That means the stack is usually Markdown plus project-local templates, not an application runtime.

## Review Gate

Review the result against:

- Codex-first positioning,
- clear separation of `AGENTS.md`, skills, `.agent/`, playbooks, and prompts,
- concrete examples,
- no invented platform behavior,
- no unnecessary complexity.
