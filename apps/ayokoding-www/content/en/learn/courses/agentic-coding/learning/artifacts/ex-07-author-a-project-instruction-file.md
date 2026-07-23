---
title: "Artifact: Minimal AGENTS.md Excerpt"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 47
---

> A minimal instruction-file excerpt declaring a build/test command and one convention, followed
> by proof the next session ran it unprompted -- exercises co-06.

```markdown
## Build & Test

\`\`\`bash
pytest tests/ -q
\`\`\`

## Conventions

- Every new function must be fully type-annotated (PEP 484).
```

Next session's tool-call log, opening line:

```text
1. run_shell(command="pytest tests/ -q")
```

No human message anywhere earlier in that session's transcript restates the test command -- the
agent read it directly from `AGENTS.md` at session start, before any file-specific work began.

**Verify**: the next session's very first tool call is `run_shell(command="pytest tests/ -q")` --
the exact command `AGENTS.md` declared -- and the transcript contains no human message repeating
that command anywhere before it -- satisfying ex-07's rule that the agent's next session runs the
declared test command without being told.
