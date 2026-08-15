---
title: "Coding round"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 11
---

## Timed artifact

Set a 42-minute timer: 20 minutes for each prompt and two minutes to close. Work without
autocomplete. Before opening the editor, record the contract, a concrete trace, chosen pattern,
invariant, and time/space cost in `code/coding-round/transcript.md`.

The two original prompts rehearse patterns already covered by [Coding
Interview](/en/learn/courses/coding-interview): pair indices (hash lookup) and compact window
(sliding window). They are not a new algorithm syllabus. Run the reference verification from this
course directory:

```bash
pytest -q code/coding-round
```

The suite is green only after the stated plan and complexity fields are present in the transcript and
both implementations satisfy their examples. Replace the reference solve with your own only after
capturing your timed attempt; compare a disagreement to the invariant, not to memorised output.
