---
title: "`local-tmp/`"
description: What local-tmp/ is for and the predicates for reclaiming anything inside it.
category: explanation
subcategory: development
tags: [temporary-files, ai-agents, file-organization, best-practices]
created: 2025-12-01
when_to_use: Use when deciding if a file belongs in local-tmp/.
---

# `local-tmp/`

**Use for**: Miscellaneous temporary files and scratch work

**Examples**:

- Draft files before finalizing
- Temporary data processing files
- Scratch notes and calculations
- Intermediate build artifacts
- Any temporary files that don't fit the "report" category

**Naming pattern**: No strict pattern required (use descriptive names)

**The directory always exists.** A tracked `local-tmp/.gitkeep` guarantees it in every clone and
worktree, so a tool that writes here never has to create it first and never fails on a missing path.
`.gitignore` ignores `local-tmp/*` and re-includes only the `.gitkeep` — everything else you put
here stays untracked. Do not delete the `.gitkeep`, and do not commit anything else in this
directory.

**Example files**:

```
local-tmp/draft-convention.md
local-tmp/temp-analysis.json
local-tmp/scratch-notes.txt
```

**Retention**: entries are reclaimable **after 7 days without modification**, and reclaiming them is
a deliberate act — never automatic. The
[build-artifact sweeper](../build-artifact-sweeper.md) does **not** touch `local-tmp/` and must not
be extended to; the directory exists precisely to hold things no ambient process is allowed to
remove.

Before deleting anything here, confirm every one of the following. Each is machine-checkable, and a
path failing any single one stays:

1. It is regenerable build output — a directory named `.next`, `dist`, `out`, `build`, `target`, or
   `node_modules` (for `.next`, it also contains a `BUILD_ID`).
2. A specific command regenerates it, and that command is recorded alongside the path.
3. Its mtime is older than 7 days.
4. It neither sits under nor contains `generated-reports/`, any `.env*` file, any git-tracked file,
   any path inside a `git worktree list` entry, or any `.git` directory.
5. No git-tracked file in either OSE repo references its path.

**Renamed captures are not artifacts.** A build directory that was renamed to record _what it
demonstrates_ — `plan04-next-webpack-failed`, `plan04-next-overlap-failure` — is evidence, and
predicate 2 is what excludes it: no command regenerates a particular past failure state. Rename
deliberately when you want output preserved, and it will fail predicate 1 on name and predicate 2 on
substance.

Reclaim by **moving** to a dated quarantine (`local-tmp/.reclaim-quarantine-YYYY-MM-DD/`) first,
then proving nothing load-bearing moved (`npm run doctor -- --fix`, `nx run rhino-cli:test:quick`,
`nx affected -t build` all exit 0), and only then deleting. Until that proof passes, the whole
operation is one `mv` from undone.
