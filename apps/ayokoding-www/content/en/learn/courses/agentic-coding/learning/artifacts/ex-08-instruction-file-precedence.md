---
title: "Artifact: Instruction-File Precedence Conflict"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 48
---

> A repo-level and a user-level instruction file declaring one conflicting rule, checked against
> Claude Code's documented memory-file loading behavior -- exercises co-06.

```markdown
# CLAUDE.md (repo-level, this project's root)

Commit messages: Conventional Commits, imperative mood, no trailing period.
```

```markdown
# ~/.claude/CLAUDE.md (user-level, global to every repo)

Commit messages: always end with a period, for consistency with my personal notes.
```

The two files state a directly conflicting rule about trailing periods on commit messages. Claude
Code's own documentation states that every discovered instruction file is **concatenated into
context, not overriding each other**, loaded broadest-scope first: managed policy, then the user's
`~/.claude/CLAUDE.md`, then the project's `CLAUDE.md` (or its `AGENTS.md` import), then any local
override file -- "so a project instruction appears in context after a user instruction." That load
order is a context-assembly order, not a conflict-resolution rule: the documentation is explicit
that when two files truly disagree, "Claude may pick one arbitrarily." So the honest, verified
answer for this pair of files is that neither rule is guaranteed to win -- a commit message from
this repo could plausibly land either with or without the trailing period, and that is the
documented behavior, not a gap in the documentation.

**Verify**: the artifact states the actual documented behavior (concatenation into context, in a
broadest-to-narrowest load order, project loaded after user) and cites the specific documented
disclaimer it relies on ("if two rules contradict each other, Claude may pick one arbitrarily") --
satisfying ex-08's rule of verifying what the agent does and citing the documented precedence
order, which for a genuine contradiction is explicitly non-deterministic rather than a fixed
override.
