---
name: project-orchestrator
description: Use when starting a substantial documentation or agent-workflow update in this guide. Handles stack-first review, Codex-first positioning, orchestration layer selection, task decomposition, review gates, and final handoff.
---

# Project Orchestrator

## Overview

This skill coordinates changes to the Agent Skills Architecture Guide. It keeps the work grounded in Codex-first orchestration while preserving clear comparisons to Claude command-folder workflows when those comparisons help the reader.

## Workflow

1. Read `AGENTS.md`.
2. Read `.agent/orchestration.md`.
3. Identify the documentation stack and affected layer:
   - `README.md` for the main paper,
   - `.agent/` for orchestration examples,
   - `skills/` for reusable capability examples,
   - `templates/` for copyable scaffolds.
4. Decide whether the request is a new section, bugfix, review, or handoff.
5. Select the matching `.agent/playbooks/` route.
6. Make the smallest useful change.
7. Review for:
   - Codex-first framing,
   - clear separation between instructions, skills, playbooks, prompts, and current task context,
   - concrete examples,
   - no invented platform behavior,
   - no unnecessary complexity.
8. Return a concise handoff with files changed, decisions made, validation, and next steps.

## Inputs

- User request.
- Current repository files.
- Any referenced Codex, Claude, or agent workflow constraints.

## Outputs

- Updated guide, playbook, skill, or template files.
- Short explanation of the architecture choice.
- Validation notes.
- Open decisions for Shane only when the work cannot safely proceed without them.

## Validation

At minimum, verify:

- expected files exist,
- Markdown headings are readable,
- examples are copyable,
- no unsupported platform claims were introduced.
