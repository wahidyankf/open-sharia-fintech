# Step 6-7: Governance Word Budget and Rules Governance

## Step 6: Governance Word Budget — Delegated

Word budgets for `AGENTS.md`, `CLAUDE.md`, and every other auto-loaded instruction surface are
owned by the deterministic `rhino-cli governance word-budget validate` gate (wired at pre-push, CI,
and as `governance-word-budget` in the `repo-governance audit` preflight, once armed). Thresholds
live only in the `governance-word-budget:` section of `repo-config.yml` — never restate them here,
since a second copy drifts from config and produces contradictory verdicts.

If `governance-word-budget` preflight is available: skip word counting entirely; read the preflight
findings and check only qualitative concerns the mechanical gate can't measure (verbose sections
where a one-line summary + `See` link would suffice, duplicate content reachable via a link,
all-at-once-complexity structure anti-patterns). If preflight is absent (fallback): read the
monitored surfaces, count words, classify against `repo-config.yml` thresholds, emit a finding for
any surface over the `fail` ceiling and an advisory for the `warn` zone.

**Remediation guidance**: the only sanctioned fix is progressive disclosure (inline content →
one-line summary + `See` link) — call out forbidden anti-fixes (deleting rules, dense compression,
splitting into another auto-loaded file) if observed. See
[Governance Word-Budget Convention](../../../../repo-governance/conventions/structure/governance-word-budget.md).

## Step 7: Rules Governance Validation

**Preflight skip annotations**: skip the traceability sub-portion if preflight covered
`traceability-audit`; skip the cross-doc layer-numbering sub-portion if preflight covered
`layer-coherence`; skip the vendor-neutrality terminology sub-portion if preflight covered
`vendor-audit`. License presence is enforced by the deterministic `rhino-cli convention license`
gate, not this preflight — never AI-re-derive it. Re-evaluate only contradictions, inaccuracies,
semantic inconsistencies, and terminology alignment.

**Scope**: all governance layers (`vision/`, `principles/`, `conventions/`, `development/`,
`workflows/`, `.claude/agents/**/*.md` content/cross-layer consistency only — frontmatter
shape/naming/mirror parity belong to `rhino-cli harness` and `repo-harness-compatibility-checker`),
`repository-governance-architecture.md`, `repo-governance/README.md`, `docs/explanation/README.md`.

1. **Contradictions**: cross-reference principle definitions against implementations, check
   conventions against each other, verify practices don't contradict the conventions they claim to
   implement, compare vision statements across documents.
2. **Inaccuracies**: validate file path references, agent/skill name references against actual
   files, layer-numbering consistency (0-5), frontmatter requirements against actual usage.
3. **Inconsistencies**: terminology alignment (e.g. "Principles Implemented" vs "Principles
   Respected"), cross-reference completeness, index-vs-directory-contents match, README-vs-detail
   alignment.
4. **Traceability**: every Principle needs "Vision Supported"; every Convention needs "Principles
   Implemented/Respected"; every Development practice needs BOTH "Principles" AND "Conventions"
   sections; every Workflow needs correct agent references.
5. **Layer Coherence**: Vision→Principles→Conventions/Development→Agents→Workflows, each layer
   properly governing/implementing the layer(s) below.
6. **Licensing Compliance** (see [Per-Directory Licensing Convention](../../../../repo-governance/conventions/structure/licensing.md)):
   every product app dir, every `libs/*` dir, and `specs/` root need MIT LICENSE;
   LICENSING-NOTICE.md table must match actual LICENSE files on disk; CLAUDE.md/README.md/ose-web
   about.md license descriptions must agree with LICENSING-NOTICE.md. Missing LICENSE = CRITICAL;
   wrong license type = HIGH; cross-doc inconsistency = MEDIUM.
7. **Dependency Bump Policy Compliance** (see [Dependency Bump Stability & Safety Policy](../../../../repo-governance/development/workflow/dependency-bump-policy.md)):
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
8. **Gherkin Step-Keyword Cardinality** (markdown fences — see
   [Acceptance Criteria Convention §Step-Keyword Cardinality](../../../../repo-governance/development/infra/acceptance-criteria/02-gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule)):
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
