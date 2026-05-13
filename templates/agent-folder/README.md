# Copyable `.agent/` Folder Template

Copy this structure into a project when you want a human-readable orchestration layer for Codex or another coding agent.

```text
.agent/
  README.md
  orchestration.md
  roles/
    architect.md
    implementer.md
    reviewer.md
    tester.md
  playbooks/
    new-feature.md
    bugfix.md
    repo-review.md
    release-handoff.md
  prompts/
    implementation-task.md
    review-task.md
    handoff-summary.md
```

Use this folder to describe how work should move through the project. Put reusable capabilities in skills. Put stable repo rules in `AGENTS.md`.
