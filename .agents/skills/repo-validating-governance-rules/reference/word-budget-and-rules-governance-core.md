# Steps 6-7: Governance Word Budget and Rules Governance (Contradictions Through Layer Coherence)

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
