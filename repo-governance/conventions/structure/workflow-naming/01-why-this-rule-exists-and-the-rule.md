---
title: "Workflow Naming: Why This Rule Exists and The Rule"
description: Why the workflow naming rule exists (checker enforceability, zero-exception discipline, semantic clarity) and the exact filename structure every workflow must match
when_to_use: Read this when you need the rationale for the workflow naming rule, or the exact filename structure every workflow must match.
category: explanation
subcategory: conventions
tags:
  - workflows
  - naming
  - conventions
created: 2026-04-17
---

# Workflow Naming: Why This Rule Exists and The Rule

## Why This Rule Exists

A uniform, exception-free naming rule gives the repository three concrete guarantees that loose naming cannot:

- **Enforceable by checker**: A single regex suffix check (`-(quality-gate|execution|setup|planning|grooming)$`) decides conformance. No per-workflow judgement, no grandfathered `-validation` holdovers, no "this one is special" carve-outs. `repo-rules-checker` can audit the entire workflow tree in one pass and produce a deterministic result.
- **Zero-exception discipline**: Exceptions erode conventions. Once one workflow is allowed a bespoke suffix, reviewers lose the ability to reject the next one on principle alone. Holding every workflow to the same structure keeps the rule teachable in one sentence and cheap to enforce forever.
- **Semantic clarity**: The suffix immediately communicates the workflow's execution model. A reader sees `*-quality-gate` and knows to expect an iterative maker → checker → fixer loop terminating on zero findings; `*-execution` is a single forward procedure; `*-setup` provisions once and exits. No body scan required.

## The Rule

Every workflow filename (basename without the `.md` extension) MUST match the structure:

```text
<scope>(-<qualifier>)*-<type>
```

Token definitions:

- **`<scope>`** — Exactly one token from the [Scope Vocabulary](./02-scope-vocabulary.md#scope-vocabulary) below, matching the parent directory under `repo-governance/workflows/`. Appears first.
- **`<qualifier>`** — Zero or more lowercase kebab tokens narrowing the scope. Each qualifier is a single hyphen-separated word or a compound kebab phrase (e.g., `rules`, `by-example`, `software-engineering-separation`). Qualifiers stack in order from broadest to narrowest.
- **`<type>`** — Exactly one token from the [Type Vocabulary](./03-type-vocabulary.md#type-vocabulary) below. Names the execution model. Appears last.

**No exceptions** (except `meta/` reference docs, below). Every workflow has exactly one scope (first) and exactly one type (last); everything between is qualifier. Filenames that cannot be parsed against this structure are governance violations regardless of history.

Additional filename rules inherit from the [File Naming Convention](../file-naming.md).
