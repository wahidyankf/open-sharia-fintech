---
description: "Repository governance validation runs in two layers — a deterministic preflight that executes mechanical checks in milliseconds, and an AI checker that handles judgement-based categories. This convention defines which layer owns which category and the contract between them."
when_to_use: "Read this index to find the right Deterministic vs AI Validation Split Convention child document."
---

# Deterministic vs AI Validation Split Convention

- [The Split — Deterministic vs AI Validation Categories](./the-split.md) — The table mapping each governance validation category to its owning layer (deterministic preflight or AI checker) and the rationale. Use when deciding, or looking up, which layer (deterministic preflight or AI checker) owns a given validation category.
- [JSON Envelope Contract](./json-envelope-contract.md) — The canonical JSON envelope shape, key order, and byte-determinism guarantees the deterministic preflight emits. Use when producing or consuming the deterministic preflight's JSON output and you need the exact schema.
- [Handoff to the AI Checker](./handoff-to-the-ai-checker.md) — How the AI checker consumes the deterministic preflight's JSON envelope, skips redundant work, and degrades gracefully when the preflight is unavailable. Use when wiring or debugging how the AI checker consumes the deterministic preflight's output.
- [Adding a New Validation Category](./adding-a-new-validation-category.md) — The decision tree for choosing a new validation category's owning layer, plus the implementation contracts for deterministic and AI-checker owners. Use when introducing a new governance validation rule and deciding which layer should own it.
- [Refactoring to Deterministic, and Out of Scope](./refactoring-and-out-of-scope.md) — The triggers for moving an AI-only category to deterministic, and what this convention deliberately does not define. Use when an AI-checker category keeps producing the same false positives and might be a candidate to become deterministic, or when checking whether a related concern is covered by this convention.
