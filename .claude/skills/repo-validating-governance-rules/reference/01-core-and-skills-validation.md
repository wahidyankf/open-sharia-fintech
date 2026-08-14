# Steps 1-5: Core Repository and Skills Quality Validation

## Step 1: Core Repository Validation

**Deterministic-gate annotation**: file naming, frontmatter shape (No-Last-Updated convention),
and emoji codepoints are enforced by the deterministic `rhino-cli md`/`convention` gates at
pre-commit and markdown CI — not in the `repo-governance audit` preflight envelope. Do not
AI-re-derive them; re-evaluate only linking correctness and semantic convention compliance not
caught mechanically.

**Path scope**: `repo-governance/**/*.md`, `.claude/agents/**/*.md`, `.claude/skills/**/*.md`,
`docs/**/*.md`, root instruction surfaces (`AGENTS.md`, `CLAUDE.md`, `README.md`), active plans
(`plans/in-progress/**/*.md`, `plans/backlog/**/*.md`). **Exempt**: website content
(`apps/ayokoding-www/`, `apps/ose-www/`, `apps/organiclever-www/`, `apps/wahidyankf-www/`),
`plans/done/` (immutable archive), generated mirrors (`.opencode/`, `.cursor/`, `.amazonq/`),
`generated-reports/`, `local-temp/`, `worktrees/`.

Validates: file naming, linking, emoji usage, convention compliance, registry-gate consistency
(live hook/CI docs delegate command discovery to `gate list`, verified by `gate validate` — flag
embedded gate inventories or retired live-CI references), and the No-Last-Updated Convention (flag
`updated:` frontmatter or `**Last Updated**` footers in non-website files — HIGH — per
[No Manual Date Metadata Convention](../../../../repo-governance/conventions/structure/no-date-metadata.md);
date fields must not exist at all, not merely be correct).

## Convergence Mechanics (applies to every step below)

**Known False Positive Skip List**: before validation, load
`generated-reports/.known-false-positives.md` if it exists; before reporting any finding, check it
against the stable key `[category] | [file] | [brief-description]` — if matched, log as
`[PREVIOUSLY ACCEPTED FALSE_POSITIVE — skipped]` (informational, not counted).

**Re-validation Mode (Scoped Scan)**: when a multi-part UUID chain exists (e.g. `abc123_def456`),
check the latest fix report for a `## Changed Files (for Scoped Re-validation)` section — if
found, run Steps 1-7 normally on all files but run Step 8 (~265 software-doc files) only on
changed files; if not found, run a full scan.

## Step 2: Agent-to-Agent Duplication Detection

**Deterministic-gate annotation**: verbatim agent/skill duplication is caught by the `rhino-cli
harness` gate — do not AI-re-derive the verbatim-match portion; re-evaluate only paraphrased/
non-verbatim duplication.

Extract content blocks (>20 lines) from all `.claude/agents/` files, compare pairwise (N×(N-1)/2
pairs), and classify: **Verbatim** (CRITICAL, exact matches ≥30 lines), **Paraphrased** (HIGH,
same knowledge different wording, ≥20 lines), **Conceptual** (MEDIUM, same concepts different
structure, ≥15 lines).

**Duplication categories**: Methodology (same validation/fixing methodology, e.g. UUID
generation/report templates — 3+ agents, 50+ lines → extract to Skill, should reference
`repo-generating-validation-reports`); Domain Knowledge (same content conventions/organization
systems — 2+ agents, 30+ lines → extract or consolidate); Tool Usage Pattern (same tool
instructions — 3+ agents, 20+ lines → extract or reference AI Agents Convention);
Criticality/Confidence (any agent defining CRITICAL/HIGH/MEDIUM/LOW inline instead of referencing
`repo-assessing-criticality-confidence` — must reference the Skill).

**Consolidation vs extraction**: prefer **Extract to Skill** when content is reusable, appears in
3+ agents, and no Skill exists yet. **Consolidate Agents** only when agents serve nearly identical
purpose, combined size <1000 lines, no loss of focus. **Keep as Duplication** only when content is
agent-specific, context genuinely requires different wording, or duplication is <10 lines.

**Criticality**: CRITICAL (50+ lines across 5+ agents), HIGH (30-49 lines across 3-4 agents),
MEDIUM (20-29 lines across 2 agents), LOW (10-19 lines, acceptable).

## Step 3: Agent-Skill Duplication Detection

**Deterministic-gate annotation**: verbatim agent/skill duplication is caught by `rhino-cli
harness` — re-evaluate only paraphrased/non-verbatim agent-Skill duplication.

For each agent, extract content blocks and compare against every Skill in `.claude/skills/`,
detecting verbatim/paraphrased/conceptual duplication and assessing criticality identically to
Step 2's scale. Common patterns to check: UUID generation logic (→
`repo-generating-validation-reports`), criticality definitions (→
`repo-assessing-criticality-confidence`), mode-parameter handling (→
`repo-applying-maker-checker-fixer`), content organization (→
`apps-ayokoding-www-developing-content`), color palettes (→ `docs-creating-accessible-diagrams`),
report templates (→ `repo-generating-validation-reports`), annotation density (→
`docs-creating-by-example-tutorials`).

## Step 4: Skill-to-Skill Consolidation Analysis

Read all Skills (exclude README.md), extract description/line-count/name-pattern/cross-references/
topic headings, and group by pattern:

- **Workflow Family**: `[prefix]-[stage]-workflow` naming covering sequential stages (3+ Skills).
- **Name Prefix Clustering**: shared prefix (`repo-*`, `docs-*`, `apps-*`, `plan-*`, `agent-*`)
  with related suffixes (2+ Skills).
- **Tiny Skill Detection**: Skills <100 lines heavily referencing a larger related Skill.
- **Topic Similarity**: 2+ Skills sharing >60% of description/heading topic keywords.
- **Sequential Dependency**: bidirectional heavy cross-referencing ("See X for..." / "See Y
  for...", >3 references each way).

**Assess each group** on: size (PASS <2000 combined lines, CONCERN 2000-3000, FAIL >3000),
cohesion (high = sequential workflow stages; medium = related but orthogonal; low = incidentally
related), usage pattern (checked via agent frontmatter — always/sometimes/rarely used together),
and progressive-disclosure benefit.

**Criticality**: CRITICAL (5+ related Skills that should be 1-2), HIGH (3-4 Skills >70% overlap,
combined <2000 lines), MEDIUM (2 Skills 50-70% overlap, trade-offs exist), LOW (optimization
suggestion, unclear benefit).

**Domain-specific exemptions — never flag**: `apps-ayokoding-www-developing-content` vs.
`apps-ose-www-developing-content` (different audiences/content despite both using Next.js 16);
`repo-assessing-criticality-confidence` vs. `repo-generating-validation-reports` (orthogonal
concerns — what to assess vs. how to report).

**Be conservative**: when unsure, recommend KEEP SEPARATE.

## Step 5: Skills Coverage Gap Analysis

Find content blocks repeated across 3+ agents with no existing Skill covering the pattern.
**Criticality**: CRITICAL (10+ agents, no Skill), HIGH (5-9 agents), MEDIUM (3-4 agents), LOW (2
agents, not yet worth extracting).

## Report Formats

**Core/general finding**: `### Finding: [type]` with Category, Files Affected, Criticality, Issue,
Evidence, Recommendation.

**Duplication finding**: `### Finding: Agent-Skill Duplication` (or Agent-to-Agent) with
Agent/Skill names, Criticality, Type (Verbatim/Paraphrased/Conceptual), Lines Duplicated,
Duplicated Content sample, and a Recommendation naming the target Skill plus the specific 3-step
fix (remove duplicated lines → add Skill to frontmatter → add a one-line "See `[skill]` for
[topic]" reference).

**Gap finding**: `### Finding: Skills Coverage Gap` with Pattern, Appears In (agent list),
Criticality, Estimated Lines, Pattern Examples, Recommendation (create new Skill or extend
existing).

**Consolidation finding**: `### Finding: Skill Consolidation Opportunity` with Skills Involved,
Criticality, Pattern Type, Current State (sizes, cross-references), Overlap Analysis, Benefits/
Risks of Merging, Recommendation (MERGE / CONSIDER MERGE / KEEP SEPARATE) with rationale and — if
MERGE — a proposed merged-file section outline.
