---
description: Explains how ignoring root causes produces compounding problems - hidden failures, multiplying patches, spreading bugs, and normalized mediocrity.
when_to_use: Use when justifying why root cause analysis is required before applying a fix.
---

# Why This Matters

Ignoring root causes produces compounding problems:

- **Symptom fixes hide real failures** - The underlying issue remains, ready to surface again under different conditions
- **Patches multiply** - Each workaround often requires another workaround, increasing complexity and coupling
- **Minimal impact violations spread bugs** - Changes that touch unrelated code introduce regressions that are difficult to associate with the original task
- **Low standards normalize mediocrity** - Accepting "good enough" work sets a baseline that degrades over time

Root cause orientation prevents these failure modes by demanding proper analysis before action and restraint in scope.
