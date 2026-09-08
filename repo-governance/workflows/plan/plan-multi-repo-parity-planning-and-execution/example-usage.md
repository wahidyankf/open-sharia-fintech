---
description: Two worked examples of invoking the composite — both parity repos, and a single-repo subset.
when_to_use: Use when constructing an invocation of this workflow or explaining its behaviour with a concrete example.
---

# Example Usage

## Default: Both Parity Repos, Plan Then Execute

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown
       gates across ose-public and ose-private"
```

The orchestrator surveys both repos, builds and grills the deviation matrix, researches and
re-grills, authors and gates one plan per repo, pushes them to each repo's `origin main`, grills the
execution specifics, then executes each plan in its repo's designated worktree (synced to
`origin/main`) as a shared DAG. A public rule or Rhino change completes before its private consumer,
while unrelated repo-specific validation may overlap within the shared N=3 agent slots when HIPPO
admits both reservations. A writer never overlaps its reader, two services never claim the same
port, and transactional/destructive work is not interrupted. On failure, new admissions stop and
in-flight work cancels only at a safe boundary before the composite reports. Each successful repo
archives its plan, repairs sibling links, and immediately removes each eligible exact
identity-recorded worktree; failed preconditions retain evidence and escalate.

## One Repo Only

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: align agent catalogs
       repos: ose-public"
```

Plans and executes only the listed repo; `ose-private` is excluded from this run.
