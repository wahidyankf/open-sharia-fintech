---
title: "Step 0.5: Deterministic Preflight — Overview"
description: What the rhino-cli repo-governance audit orchestrator does (four fixed-order categories), and why the step is numbered 0.5 instead of renumbering Steps 1-6.
when_to_use: Use when understanding what the deterministic preflight covers before invoking it.
---

# Step 0.5: Deterministic Preflight — Overview

Run the `rhino-cli` orchestrator to harvest the deterministic governance findings before invoking the AI checker. The `repo-governance audit` orchestrator runs exactly **four** governance categories in fixed order — `layer-coherence`, `traceability-audit`, `vendor-audit` (the last scoped to `repo-governance/` prose plus the `AGENTS.md` and `CLAUDE.md` root instruction surfaces), and `governance-word-budget` (word budget check on all auto-loaded instruction surfaces per the `governance-word-budget:` section in `repo-config.yml`) — normalises their findings into one JSON envelope, and caches via Nx. The other deterministic markdown/convention/harness validators (file naming, frontmatter shape, license presence, README index integrity, emoji codepoints, heading hierarchy, agent-skill verbatim duplication, gherkin-keyword-cardinality) live under sibling `rhino-cli` subcommands (`md`, `convention`, `harness`, `governance`, `specs`) and are enforced by the markdown and commit gates — they are not part of this preflight. The AI checker then runs only the AI-only categories (paraphrased duplication, semantic contradictions, terminology alignment, principle-appropriateness judgement).

**Why Step 0.5 (and not Step 1, renumbering everything down)**: This step was inserted between the pre-existing Step 1 (Initial Validation) and the workflow start. Decimal numbering preserves the existing Step 1-6 references in the checker/fixer prompts that pre-date the preflight. The [Workflow Identifier Convention](../../meta/workflow-identifier.md) explicitly allows sub-step decimals for non-disruptive insertions.

**Continued in** [Step 0.5: Deterministic Preflight — Command and Exit Handling](./step-0-5-deterministic-preflight-continued.md).
