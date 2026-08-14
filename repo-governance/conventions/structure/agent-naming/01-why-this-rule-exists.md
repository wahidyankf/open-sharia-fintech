---
title: "Agent Naming Convention — Why This Rule Exists"
description: The three guarantees a uniform, exception-free agent filename rule provides — checker enforceability, zero-exception discipline, and harness parity.
when_to_use: Use when you need the rationale for why agent filenames follow one exception-free rule.
category: explanation
subcategory: conventions
tags:
  - agents
  - naming
  - conventions
created: 2026-04-17
---

# Why This Rule Exists

A uniform, exception-free naming rule gives the repository three concrete guarantees that loose naming cannot:

- **Enforceable by checker**: A single regex suffix check (`-(maker|checker|fixer|dev|deployer|manager|tester|researcher)$`) decides conformance. No per-agent judgement, no grandfathered legacy names, no "this one is special" carve-outs. `repo-rules-checker` can audit the entire population in one pass and produce a deterministic result.
- **Zero-exception discipline**: Exceptions erode conventions. Once one agent is allowed a bespoke suffix, reviewers lose the ability to reject the next one on principle alone. Holding every agent to the same structure keeps the rule teachable in one sentence and cheap to enforce forever.
- **Harness parity**: The coding agent reads the primary binding directory (`.claude/agents/*.md`); secondary binding directories (e.g., `.opencode/agents/*.md`) mirror this structure. The sync pipeline assumes a filename-for-filename mirror between the two directories. Drift in either direction — a rename in one directory but not the other, a primary agent with no secondary twin — breaks cross-harness invocation silently. A shared naming rule makes the mirror check a trivial set-difference.
