# Step 0.5: Consume Deterministic Preflight

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
