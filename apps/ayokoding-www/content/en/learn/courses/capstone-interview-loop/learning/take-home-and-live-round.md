---
title: "Take-home and live round"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 21
---

## Timed artifact

Treat `code/take-home/` as a fresh checkout. Its README is the reviewer-facing contract and its
focused tests are the clean-checkout proof. First read the brief, identify an explicitly small scope,
run the stated command, and make any choices or cuts legible.

Then use `code/live/transcript.md` for a narrated 25-minute shared-editor session. Start with a
clarifying question, keep each checkpoint runnable, and say why you are changing an increment. The
live file is deliberately small: it rehearses collaborative sequencing from [Take-Home & Live
Coding](/en/learn/courses/take-home-and-live-coding), not a new framework or product problem.

```bash
pytest -q code/take-home code/live
```

If a test fails, say what evidence you have, make the smallest repair, and rerun the narrow command.
Do not silently rewrite the session after the fact.
