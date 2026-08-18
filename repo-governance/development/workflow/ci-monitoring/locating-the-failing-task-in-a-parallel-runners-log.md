---
title: "Locating the Failing Task in a Parallel Runner's Log"
description: Why the tail of a parallel Nx runner's log belongs to whichever task finished last, not the one that failed, and how to find the real failure.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use when diagnosing a failed CI job whose log is produced by a parallel task runner like Nx.
---

# Locating the Failing Task in a Parallel Runner's Log

**Never diagnose a failed job from the tail of its log.** Nx runs tasks in parallel and flushes each
task's captured output when that task completes, so the last block in the log belongs to whichever
task finished **last** — not to the one that failed.

This breaks the usual "read the bottom of the log" habit in the most misleading direction: the tail
appears to stop mid-stream, which reads as a crash or an OOM kill. A real occurrence in this repo was
triaged three times as a silent crash under runner contention. The truncated-looking tail was a
_passing_ task's output; the failure was four blocks earlier and its actual cause was a one-line
`rustup` message.

**Do**: locate the failing unit by its status marker first, then read only that block.

```bash
gh run view --log --job=<id> | grep -E '^##\[group\](✅|❌)'
```

Every `##[group]❌ > nx run <project>:<target>` line is a failing task; anything else is noise. Treat
"the log ends mid-stream" as a statement about **flush order**, not about the process. The same
caution applies to any task runner that buffers and interleaves per-task output.
