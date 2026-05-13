# `.agent/` Orchestration Folder

This folder is the project-local operating map for agent workflows.

It is intentionally not a replacement for Codex skills. Skills define reusable capabilities. This folder defines how those capabilities are sequenced for this project.

## Folder Map

```text
.agent/
  README.md
  orchestration.md
  roles/
  playbooks/
  prompts/
```

Use this folder when a user or orchestration agent needs to know:

- which role should handle a task,
- which playbook should be followed,
- which skills should be loaded,
- what review gates are required,
- what the final handoff should include.
