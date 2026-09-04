---
name: rules-propagation
title: "rules-propagation"
description: "Places newly-stated rules on the correct surface — instruction surface first, governance layers below — de-conflicting, deduplicating, arming enforcement."
when_to_use: "Use when a decided rule must be written into the repository, or an existing rule superseded."
goal: Land every stated rule correctly, contradicting nothing, retaining no unjustified duplicate, carrying an enforcement disposition
termination: "No-op verified, or PR green with every rule placed and dispositioned; halts on an unfalsifiable rule or a higher-layer conflict"
inputs:
  - name: rules
    type: string
    description: "Rules as free prose, normalized at Step 0"
    required: true
  - name: mode
    type: enum
    values: [lax, normal, strict, ocd]
    description: "Threshold for the Step 8 quality gate"
    required: false
    default: strict
  - name: max-concurrency
    type: number
    description: "Concurrent background agents — the N in the N+1 model"
    required: false
    default: 3
  - name: isolation
    type: enum
    values: [current, dedicated]
    description: "Use the caller's tree, or create a worktree for the run"
    required: false
    default: current
  - name: dry-run
    type: boolean
    description: "Emit the manifest and conflict report, write nothing"
    required: false
    default: false
outputs:
  - name: placement-manifest
    type: file
    pattern: local-tmp/rules-propagation/rules-propagation__*__manifest.md
    description: "Subject inventory with per-surface verdict, canonical home or replacement, keep rationale; plus placement, layer, enforcement, supersessions"
  - name: final-status
    type: enum
    values: [no-op, landed, halted, partial]
    description: Terminal state of the run
  - name: pr-url
    type: string
    description: PR opened by the run
  - name: sibling-obligation
    type: string
    description: "Obligation naming the sibling repository, or an explicit none"
---

# Repository Rules Propagation Workflow

Rules arrive as free prose. They are normalized into falsifiable statements, routed to the
narrowest surface that binds, checked against existing rules under layer-aware precedence,
consolidation-reviewed within their subject, and dispositioned for enforcement. The run works in the
caller's current tree by default.

The instruction surface is a **fixed-size cache**: an admission without enough headroom requires
eviction. A threshold is never raised to make room for a placement. A separately justified,
class-wide policy recalibration follows the governance word-budget convention and is not an
eviction substitute.

**Semantic-preservation hard gate:** a word budget may change placement, never meaning. Propagation
must preserve every obligation, audience qualifier, scope boundary, exception, pass condition, and
violation condition verbatim enough to remain unambiguous. It may use progressive disclosure or an
indexed split; it may not generalize, weaken, compress away, or paraphrase a material qualifier to
make a counter pass. For example, “junior engineer fresh from bootcamp with no professional work
experience” cannot become merely “new engineer” for brevity.

Agents composed: `.claude/agents/repo/repo-rules-maker.md`, `repo-rules-checker`,
`repo-rules-fixer`. `rules-quality-gate` verifies at Step 8.

## Contents

- [Purpose and Scope](./rules-propagation/purpose-and-scope.md) — what it places, what it refuses.
- [Execution Mode](./rules-propagation/execution-mode.md) — delegation and invocation.
- [Step 0: Intake](./rules-propagation/step-0-intake-and-normalization.md) — prose to falsifiable rule.
- [Step 1: Working Tree](./rules-propagation/step-1-worktree-and-branch.md) — where the run writes.
- [Step 2: Classification](./rules-propagation/step-2-classification.md) — subject, layer, neutrality.
- [Step 3: Semantic Sufficiency and Conflict Scan](./rules-propagation/step-3-conflict-scan.md) — semantic no-op, precedence, supersession.
- [Step 4: Placement](./rules-propagation/step-4-placement-decision.md) — admission test, home table.
- [Step 5: Eviction](./rules-propagation/step-5-eviction-protocol.md) — making room on a full surface.
- [Step 6: Write and Tidy](./rules-propagation/step-6-write-and-tidy.md) — classify, consolidate, reindex.
- [Step 7: Enforcement](./rules-propagation/step-7-enforcement-disposition.md) — the mandatory three-way outcome.
- [Step 8: Verification](./rules-propagation/step-8-verification.md) — bindings, gates, quality gate.
- [Step 9: Delivery](./rules-propagation/step-9-delivery-and-sibling-obligation.md) — PR, recorded obligation.
- [Termination Criteria](./rules-propagation/termination-criteria.md) — landed, halted, partial.
- [Success Criteria](./rules-propagation/success-criteria.md) — Gherkin.
- [Safety Features](./rules-propagation/safety-features.md) — guards on destructive authority.
- [Example Usage](./rules-propagation/example-usage.md) — worked invocations.
- [Related Workflows](./rules-propagation/related-workflows.md) — what runs before and after it.
- [Principles Implemented/Respected](./rules-propagation/principles-implemented-respected.md) — traceability.
- [Conventions Implemented/Respected](./rules-propagation/conventions-implemented-respected.md) — traceability.
