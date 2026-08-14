# Preflight Consumption, Execution Sequence, and Report Structure

## Step 0.5: Consume Deterministic Preflight

**Input**: `preflight-report` argument — path to `generated-reports/repo-governance-audit__*.json`,
produced by the orchestrating workflow (`repo-governance/workflows/repo/repo-rules-quality-gate.md`)
running `./apps/rhino-cli/dist/rhino-cli repo-governance audit -o json`.

**Procedure**:

1. Read the preflight JSON.
2. Validate envelope: confirm `schema` equals `rhino-cli/repo-governance-audit/v1`. If missing/
   different, treat preflight as absent and run all Steps 1-8 in full (defensive fallback).
3. Extract findings: parse `result.categories[]` (`name`, `command`, `passed`, `findings[]`) and
   `result.skipped_false_positives[]`.
4. Populate the deterministic skip set. The orchestrator emits exactly four categories, each
   marking a step/sub-step already covered by `rhino-cli` and never re-evaluated by the AI checker:

   | Preflight category       | Step covered (skip)                                                   |
   | ------------------------ | --------------------------------------------------------------------- |
   | `layer-coherence`        | Step 7 layer-coherence portion                                        |
   | `traceability-audit`     | Step 7 traceability portion (Vision/Principles/Conventions)           |
   | `vendor-audit`           | Step 7 vendor-neutrality portion (governance prose terminology)       |
   | `governance-word-budget` | Step 6 word-count portion (never re-derive sizes; defer to preflight) |

   **Not in this envelope**: file naming, frontmatter shape, emoji codepoints, heading hierarchy,
   README index integrity, license presence, and agent/skill verbatim duplication run under the
   sibling `rhino-cli md`, `convention`, and `harness` subcommands (pre-commit/CI gates) — the
   per-step "deterministic-gate annotation" notes say which gate owns each.

5. Embed preflight findings verbatim under a new `## Deterministic Findings (rhino-cli preflight)`
   section, before `## AI-Only Findings`. Each renders with the same key/severity/criticality/
   file/line/message shape as a regular finding.
6. Re-validation optimization: compute `sha256(preflight-json-bytes)`. If identical to the prior
   iteration's hash (stored at `generated-reports/.preflight-hash-<uuid-chain>`), reuse the prior
   deterministic-findings section unchanged and only re-evaluate AI-only categories; store the new
   hash for next time.

**On failure** (argument missing, file absent, or schema mismatch): log a `[WARN]` explaining
preflight was unavailable, then run Steps 1-8 in full as fallback.

## Execution Sequence

Step 0 (initialize report — UUID/timestamp/progressive writing, see
`repo-generating-validation-reports` Skill) → Step 0.5 (preflight, above) → Step 1 (Core
Repository) → Step 2 (Agent-to-Agent Duplication) → Step 3 (Agent-Skill Duplication) → Step 4
(Skill-to-Skill Consolidation) → Step 5 (Skills Coverage Gaps) → Step 6 (Word Budget) → Step 7
(Rules Governance) → Step 8 (Software Docs) → Step 9 (Finalize: status → "Complete", summary
statistics per category — Core Repository, Agent-to-Agent, Agent-Skill, Skill Consolidation,
Skills Gaps, Word Budget, Rules Governance, Software Docs).

## Final Audit Report Structure

When preflight succeeded, the report has two top-level sections in fixed order:

1. **`## Deterministic Findings (rhino-cli preflight)`** — every preflight finding, grouped under
   per-category H3 headings mirroring `result.categories[]` order:

   ```markdown
   ### [SEVERITY] [CRITICALITY] <category> — <file>:<line>

   **Key**: `<category>|<file>|<short-hash>`
   **Message**: <message>
   **Source**: `rhino-cli repo-governance <category> validate` (preflight)
   ```

   Skipped false-positives go under `### [INFO] Skipped (known false positives)`.

2. **`## AI-Only Findings`** — output of the AI-only sub-portions of Steps 1-8 (paraphrased
   duplication, contradictions, terminology alignment, semantic principle-appropriateness, README
   content quality, etc.), each using its step's finding format.

When preflight is unavailable, use a single `## Findings` section covering the full Steps 1-8
evaluation — the pre-preflight format.

## Important Notes

**Progressive writing** is mandatory for every step, not just Step 8 — findings written
immediately survive compaction; buffered findings don't.

**Duplication detection accuracy**: favor high-confidence matches; false positives are acceptable
since the fixer re-validates before applying.

**Performance**: Agent-Skill comparison is O(agents × skills); Agent-to-Agent and Skill-to-Skill
are O(n²/2) — use efficient text matching, never character-by-character.

**Thresholds**: only suggest a new Skill for patterns in 3+ agents; only suggest Skill
consolidation when benefits clearly outweigh risk (combined <2000 lines, high cohesion, always used
together) — when uncertain, KEEP SEPARATE.
