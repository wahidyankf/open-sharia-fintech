---
title: "Build and Verify"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

1. Build a provider adapter and fake response stream around a read-evaluate-act loop.
2. Register read, write, and test tools; deny tools outside the approved workspace.
3. Compact context at a fixed budget, and write an audit event before each approved tool action.
4. Add trace, latency, and evaluation records plus an approval gate in the terminal UI.
5. Start from a failing local test and show the fake-backed loop reaches green without a network call.

The implementation below is deliberately small: it proves the seams and leaves live provider wiring,
vector storage, and browser research to their owning courses.

```python
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Action:
    tool: str
    path: str

def approve(workspace: Path, action: Action) -> bool:
    candidate = (workspace / action.path).resolve()
    return action.tool in {"read", "test"} and candidate.is_relative_to(workspace.resolve())

def run_fake(workspace: Path, action: Action) -> dict[str, str]:
    if not approve(workspace, action):
        return {"status": "denied", "audit": f"denied:{action.tool}:{action.path}"}
    return {"status": "ok", "audit": f"approved:{action.tool}:{action.path}"}
```

## Evidence to keep

Keep the failing and passing test output, budget decision, approval decision, trace identifier, and
audit log. Do not put tokens, prompts containing secrets, or unbounded shell output in those records.
