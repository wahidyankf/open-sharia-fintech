---
title: "Platform Binding Compatibility and Industry Convention"
description: How the WorktreeCreate hook stays platform-agnostic across coding agent platforms, and why this convention deliberately departs from the industry-standard sibling-directory worktree placement
when_to_use: Read this when checking cross-platform hook compatibility, or when you need the rationale for placing worktrees inside the repo instead of as sibling directories.
category: explanation
subcategory: conventions
tags:
  - worktree
  - git
  - repository-structure
  - claude
  - hooks
created: 2026-05-03
---

# Platform Binding Compatibility and Industry Convention

## Platform Binding Compatibility

```binding-example
The WorktreeCreate hook is registered in ~/.claude/settings.json. The Claude Code coding agent supports this hook event natively (see https://code.claude.com/docs/en/hooks for the field schema and transport contract); other coding agent platforms that support a `WorktreeCreate` hook with the same JSON-on-stdin contract reuse the same shell script without modification.
```

The hook script itself is platform-agnostic bash with `jq` for JSON parsing (`jq` is part of the doctor minimal toolchain per AGENTS.md), ensuring compatibility across platforms.

## Industry Convention vs. Chosen Approach

The dominant industry convention (per GitWorktree.org, Tower docs, Beej's Guide) places worktrees as **sibling directories** next to the main clone, not inside it:

```
~/projects/
├── myapp/                  # main worktree (original clone)
├── myapp-feature-auth/     # sibling worktree (outside repo)
```

This approach avoids nested-`.git` issues, keeps tools that walk up the directory tree happy, and is the most widely recommended pattern.

**Why `/worktrees/` inside the repo instead:**

- **Hook constraint**: The `WorktreeCreate` hook receives `cwd` (the project root) and resolves paths relative to it. Routing to a sibling path requires computing `..` from the repo root, which is messier and less portable across machines.
- **Dual-platform support**: A single hook registered in `~/.claude/settings.json` serves both platforms without duplication.
- **Simplicity**: Keeping worktrees inside the repo root makes `git worktree list` output scannable and keeps all repo-related state in one place.
- **Future-proofing**: If either platform adds native sibling-path support, this convention can be updated without changing the hook logic.

This is a deliberate pragmatic trade-off, not a lack of awareness of the sibling convention. Revisit if tooling problems emerge.
