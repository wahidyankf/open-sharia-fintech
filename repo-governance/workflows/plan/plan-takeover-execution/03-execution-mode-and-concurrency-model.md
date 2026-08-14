---
title: "Execution Mode and Concurrency Model"
description: States that this workflow runs as direct orchestration with no delegated discovery agent, and how the N+1 concurrency model applies across repos and cleanup candidates.
when_to_use: Use when determining whether discovery probes should fan out across repos, or how many background agents may run concurrently during takeover.
---

# Execution Mode and Concurrency Model

## Execution Mode

**Direct Orchestration** — the calling context is the orchestrator throughout discovery,
reconciliation, cleanup, and handoff, exactly as in `plan-execution.md` and
`multi-plans-execution.md`. There is no delegated discovery agent: the git/`gh` probes in Phase A are
read-only and cheap enough to run directly, and delegating them would add a context hop without
adding judgment.

## Concurrency Model

The same **N+1 model** applies — `1 main thread + N background agents = N+1 total`, default **N=3**,
per the [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md).
Within one repo, discovery is largely sequential: a found branch name changes what the next probe
searches for (e.g., a discovered PR's `headRefName` narrows the branch-list query), so probes run in
the stated order rather than all at once. Across repos, independent repos' probe sets MAY fan out as
parallel background Tasks up to N when `repos` resolves to more than one entry. Phase D's cleanup
candidates are independent of each other by construction (each is a distinct worktree/branch) and may
also fan out up to N.
