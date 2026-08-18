# Step 7 (continued): Licensing, Dependency Bump Policy, Gherkin Cardinality, Report Format

1. **Licensing Compliance** (see [Per-Directory Licensing Convention](../../../../repo-governance/conventions/structure/licensing.md)):
   every product app dir, every `libs/*` dir, and `specs/` root need MIT LICENSE;
   LICENSING-NOTICE.md table must match actual LICENSE files on disk; CLAUDE.md/README.md/ose-web
   about.md license descriptions must agree with LICENSING-NOTICE.md. Missing LICENSE = CRITICAL;
   wrong license type = HIGH; cross-doc inconsistency = MEDIUM.
2. **Dependency Bump Policy Compliance** (see [Dependency Bump Stability & Safety Policy](../../../../repo-governance/development/workflow/dependency-bump-policy.md)):
   scan every plan (backlog/in-progress/done) that introduces or modifies dependency versions:
   - Three-path classification (LTS/60-day-soak/security-waiver) required in `tech-docs.md` —
     unclassified = HIGH.
   - Rule 5a/Recency: pinned version must be the most recent eligible for its path — HIGH if not.
   - Rule 5b/Functional Stability: clearance status must be `CLEAR`, `CLEAR (patch-of)`, `WAIVER`,
     or `FUNCTIONAL-HOLD` (any may carry `(KEV-listed)` when actively exploited at bump time);
     yanked/deprecated/blocked versions require `FUNCTIONAL-HOLD` with skipped version + fallback +
     reason. Missing/incorrect status = HIGH; `FUNCTIONAL-HOLD` without detail = MEDIUM.
   - Security Clearance Status table required in `tech-docs.md` — absence = HIGH.
   - Exact pinning only, no `^`/`~` (verify: `grep -E '"\^|"~' <file>`) — violation = CRITICAL.
   - Path C waivers must be registered in `docs/reference/security-waivers.md` — missing = HIGH.
   - `FUNCTIONAL-HOLD` statuses must be registered in the same file's FUNCTIONAL-HOLD table —
     missing = HIGH.
   - `(KEV-listed)` statuses need KEV `dateAdded`/`knownRansomwareCampaignUse` fields there —
     missing = HIGH.
   - CVSS ≥ 7.0 needs a recorded EPSS score/percentile — missing = MEDIUM; EPSS ≥ 0.5 requires Path
     C urgency — lower path without waiver justification = HIGH.
   - Scope note: for `plans/done/`, flag only CRITICAL/HIGH (historical accuracy); for
     `plans/in-progress/`/`plans/backlog/`, flag all severities.
3. **Gherkin Step-Keyword Cardinality** (markdown fences — see
   [Acceptance Criteria Convention §Step-Keyword Cardinality](../../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule)):
   scope is ` ```gherkin ` fences in `repo-governance/`, `docs/`, `.claude/skills/`, and active
   plans (`plans/done/` exempt; tracked `.feature` files use the deterministic
   `gherkin-keyword-cardinality` linter instead). Per `Scenario`, count primary
   `Given`/`When`/`Then` lines (`And`/`But`/`*` never count; `Background` and `Examples` tables are
   exempt) — flag more than one primary keyword of the same type unless the fence carries an
   explicit deliberate-example label. Unlabeled violation = HIGH; missing label on an intentional
   counter-example = MEDIUM.

**Report format**: `### Finding: [Contradiction/Inaccuracy/Inconsistency/Traceability
Violation/Layer Coherence]` with Category, Files Affected, Criticality, Issue, Evidence,
Recommendation — write all findings progressively during Step 7, using the same shape for each
sub-category above.
