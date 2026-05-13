# Implementation Task Prompt

Use this prompt when asking Codex or a worker agent to implement a bounded change.

```text
You are working in this repository as an implementation agent.

Read AGENTS.md first.
Then read the relevant .agent playbook.

Task:
{specific task}

Scope:
{files or folders the agent may edit}

Acceptance criteria:
{observable completion criteria}

Do not change unrelated files.
List every file changed in your final response.
```
