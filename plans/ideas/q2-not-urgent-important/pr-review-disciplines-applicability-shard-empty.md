# PR-review disciplines "Applicability and Finding Disposition" shard is empty

One-line summary: `pr-review-disciplines/applicability-and-finding-disposition.md`'s frontmatter
promises rules for when the nine reviewer disciplines run and how findings are disposed; the body
is a truncated duplicate of the parent index's navigation list and defines neither concept anywhere
in the tree.

> Surfaced 2026-08-18 during PR #227's cycle-1 review, examined and ruled pre-existing.

## Problem / context

`repo-governance/development/quality/pr-review-disciplines/applicability-and-finding-disposition.md`
carries a `when_to_use` promising rules for "when the PR-review specialist disciplines run at all,
and how code-related vs LOW findings are disposed", but its body is an odd `.././pr-review-disciplines/`
relative-path nav list copied from the parent `README.md`. Grepping the tree for "Finding
Disposition" outside this file returns exactly one hit: the parent `README.md`'s annotation
promising this file's content — a promise with nothing behind it. Diffing against the base-commit
predecessor (`repo-governance/development/quality/pr-review-disciplines/01-applicability-and-finding-disposition.md`
at `3b5349a97`) shows the body is byte-identical; only the `NN-` ordinal-stripping rename touched
this file, so the gap predates the sweep that renamed it.

## Why now

Low urgency: nothing currently reads this shard expecting the missing rules to be enforced, and no
gate depends on its content existing. It stays open because the nine-discipline PR-review cycle is
the default merge gate on every `*-to-pr` delivery, so an agent that DOES go looking for the
applicability/disposition rule here finds nothing and either invents behavior or stalls.

## Prior art / precedents

- **Parent index** — [`pr-review-disciplines/README.md`](../../../repo-governance/development/quality/pr-review-disciplines/README.md)
  carries the annotation promising this shard's content; the promise and the gap live one hop apart.
- **`pr-review-quality-gate` workflow** — [pr-review-quality-gate.md](../../../repo-governance/workflows/pr/pr-review-quality-gate.md)
  is the closest thing to a live disposition rule today (loop-exit/escalation rules), but it is not
  what this shard's frontmatter claims to be.
- **`pr-review-synthesis-maker`** — [pr-review-synthesis-maker.md](../../../.claude/agents/pr-review/pr-review-synthesis-maker.md)
  is where "how code-related vs LOW findings are disposed" is actually decided today, informally, in
  agent prose rather than in this shard.

## Proposed direction (sketch)

Either write the promised content (a short shard stating when each of the nine disciplines is
in-scope for a given PR, and the LOW-vs-code-related disposition split already implicit in
`pr-review-synthesis-maker`'s triage), or retire the shard and its `README.md` promise together if
the content is judged redundant with the workflow doc.

## Rough scope & non-goals

In scope: this one shard, its parent `README.md` annotation, and any other file whose `README.md`
promises content this shard doesn't have.

Out of scope: rewriting the nine-discipline pipeline itself, or the loop-exit/escalation rules that
already live in `pr-review-quality-gate.md`.

## Risks & open questions

- Whether the disposition rule belongs here at all, or is more honestly a `pr-review-fixer-resolution`
  skill concern (the four-way triage already lives there) — needs a placement decision before
  drafting content.
- Low risk of silent scope creep: this is a documentation-only gap with no code or gate dependency.

## What success looks like + promotion signal

Success: the shard's body matches its frontmatter's promise, or the promise and the empty shard are
both removed. Ready to promote once someone decides whether the content belongs in this shard, in
`pr-review-quality-gate.md`, or in the `pr-review-fixer-resolution` skill — that placement call is
the gate, not the writing.
