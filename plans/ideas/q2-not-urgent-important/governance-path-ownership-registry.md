# Governance path-ownership registry

One-line summary: declare which agent owns which path in a machine-checked registry, instead of
asserting scope in prose inside 50-58 KB agent files that drift per repo — then close the five
zero-owner gaps the declaration exposes.

> Idea, added 2026-08-05.

## Problem / context

Checker scope in this repo is asserted three times over, in three places that disagree.

A 2026-08-05 audit of `repo-rules-checker` found **eight** internal contradictions in its declared
scope. The most dangerous: a free-floating `### AGENTS.md Size Monitoring` section hard-coded
"Target 30,000 / Warning 35,000 / Hard Limit 40,000 (DO NOT EXCEED)" while `repo-config.yml` sets
`AGENTS.md` to `target: 24000 / warn: 27000 / fail: 30000`. A 35,000-byte file was simultaneously
"Warning" and a hard FAIL depending on which authority you read. **That trap fired live** during the
build-artifact-sweeper work the same day. Those eight contradictions were fixed directly (ose-public
`8f4e211e5`), but the fix is per-file prose — nothing prevents the next drift.

Underneath the contradictions sits the structural cause: **there is no mechanical check that two
agents do not claim the same path, and no check that a path has any owner at all.** Enforcement
across the agent catalog is naming-only (`rhino-cli harness naming validate`). The `<scope>` token in
an agent's filename (`repo-`, `docs-`, `swe-`, …) is a _naming_ namespace, not a filesystem-ownership
one — which is exactly why `repo-rules-checker` and `docs-software-engineering-separation-checker`
can both claim `docs/explanation/software-engineering/` without tripping any gate.

The audit found four undocumented overlaps and five zero-owner paths:

**Undocumented overlaps** (neither file names the other):

| Path                                       | Claimants                                                                                      |
| ------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| `repo-governance/workflows/**`             | `repo-rules-checker` vs `repo-workflow-checker` — the latter declares **no path scope at all** |
| `docs/explanation/software-engineering/**` | `repo-rules-checker` Step 8 vs `docs-software-engineering-separation-checker`                  |
| `apps/**` + `libs/**` Nx targets and tags  | `ci-checker` vs `swe-code-checker` run near-identical checks                                   |
| every `README.md` in the repo              | `readme-checker` declares no path bound, so it implicitly claims all of them                   |

**Zero-owner paths**:

1. `.claude/hooks/**` — referenced by no checker in the repo
2. `.cursor/**` — exists on disk, absent from the harness parity invariant and every catalog check
3. `.claude/settings.json` internals — only read as a catalog row to diff, never validated
4. links inside `.claude/skills/**` — **explicitly skipped** by the link validator
   (`application/docs/links.rs:483-486`), and covered by nothing else
5. README-index integrity for `docs/` generally, `specs/`, and `plans/` — the validator's default
   paths cover only `repo-governance/`, `.claude/agents/`, `.claude/skills/`, and the
   software-engineering docs subtree

## Why now

Two forces converge.

**The prose approach has demonstrably failed at scale.** The checker is 49-58 KB depending on repo
and has drifted in all four. Scope lives in prose in every copy, so a scope decision must be
re-authored four times and can silently diverge — which it has.

**The mechanism to fix it is arriving anyway.** `sdlc-gate-registry-enforcement` (in progress,
readiness item R10 pending) introduces a central **gate registry** in `repo-config.yml`, with
`rhino-cli gate list` / `gate emit` already present in the CLI. It spans the same four repos and
edits the same file. An ownership registry is the same shape of solution and should reuse that
infrastructure rather than invent a competing one.

## Prior art / precedents

- **Deterministic vs AI Validation Split Convention** — the existing rule that mechanical checks
  belong in `rhino-cli` and judgement-based ones in the AI checker. An ownership registry is the
  missing third axis: _which agent_, alongside _which tier_.
  [split convention](../../../repo-governance/conventions/structure/deterministic-vs-ai-validation-split.md)
- **`sdlc-gate-registry-enforcement`** — the plan that landed the central-registry-in-`repo-config.yml`
  pattern this should extend. [plan](../../done/2026-08-07__sdlc-gate-registry-enforcement/README.md)
- **Instruction-File Size Budget Convention** — precedent for thresholds living in `repo-config.yml`
  as the single authority, with agent prose deferring to it rather than restating it. The 40k-vs-30k
  contradiction is what happens when that deference lapses.
  [budget convention](../../../repo-governance/conventions/structure/governance-word-budget.md)
- **AI Agents Convention** — states "clear responsibilities to avoid overlap with other agents" as a
  principle, but provides no per-path registry to enforce it.
  [ai-agents](../../../repo-governance/development/agents/ai-agents.md)

## Proposed direction (sketch)

Approved direction as of 2026-08-05: **declare the boundary, do not widen it.**

**A1 — Ownership registry.** An `ownership:` map in `repo-config.yml`: glob → owning agent →
dimension (`format` | `content` | `parity` | `factual`). A new
`rhino-cli repo-governance ownership validate` fails on any path with zero owners, or two owners
claiming the same _dimension_ on the same glob. Different dimensions on one path stay legal — that is
the existing, working `repo-rules` (format) / `docs-checker` (factual) / `docs-link-checker`
(reachability) split, which the registry records rather than disturbs. Agent prose then cites the
registry instead of restating scope.

**A2 — `repo-rules-*` formally owns the governance surface**, content-and-consistency dimension only:
`repo-governance/**`, `.claude/{agents,skills,hooks}/**`, `.claude/settings.json`, `AGENTS.md`,
`CLAUDE.md`. Byte size, links, anchors, naming, and frontmatter stay deterministic — the AI checker
never re-derives what a Rust validator already proves.

**A3 — the `docs/` split stays as it is, but becomes explicit.** `repo-rules` keeps the
software-engineering subtree (format/structure), `docs-checker` keeps factual accuracy,
`docs-link-checker` keeps reachability, `docs-tutorial-checker` keeps pedagogy. Retire or narrow the
standing backlog line proposing that `repo-rules-checker` absorb all of `docs/`.

**A4 — close the five zero-owner gaps**, most of them cheap: un-skip `.claude/skills/` in the link
validator, add `.claude/hooks/**` and `settings.json` to `repo-rules` scope, widen the
`readme-index` default paths, and add `AGENTS.md`/`CLAUDE.md` to the CI vendor-audit invocation
(today they are vendor-scanned only under `repo-governance audit`, which is not in GitHub CI).

**A5 — resolve the contradictions first.** Done for six of eight in ose-public (`8f4e211e5`);
propagation to the siblings follows.

## Rough scope & non-goals

**In scope**: `repo-config.yml` schema addition; one new `rhino-cli` validator with Gherkin specs;
scope-section edits in the affected agent definitions; the five gap closures; both parity repos.

**Non-goals**:

- **Not** a consolidation of the `docs-*` agent family into `repo-rules-*`. That was considered and
  declined — it collides with four agent families and the deterministic-vs-AI split for a simplicity
  gain the registry delivers more cheaply.
- **Not** a widening of any AI checker's path list. The registry records today's boundaries; moving
  one is a separate, deliberate decision per path.
- **Not** a replacement for the gate registry. This is a follow-on that reuses it.

## Risks & open questions

- **Sequencing is the main risk.** Running this concurrently with `sdlc-gate-registry-enforcement`
  means two plans editing `repo-config.yml` across four repos with two competing registry designs.
  Decided: this waits for that plan to land.
- **Dimension vocabulary needs to be right first time.** `format`/`content`/`parity`/`factual` is a
  sketch; getting it wrong forces a second migration through four repos.
- **The registry could ossify a wrong boundary.** Declaring today's overlaps makes them official.
  Mitigation: the four undocumented overlaps get an explicit decision each — record or resolve —
  rather than being auto-imported.
- **Open**: does `beaver-nest`'s forked `rhino-cli` track this validator, or diverge? It sits outside
  the byte-identity boundary that binds the other three.
- **Open**: should the registry cover `plans/**`, where `plan-checker` and `repo-rules-checker` both
  operate today?

## What success looks like + promotion signal

**Success**: every path in the repo has exactly one owner per dimension, asserted in one file per
repo; a new agent cannot silently claim occupied territory; the five gaps are closed; and an agent's
prose scope section can no longer contradict the registry because it no longer restates it.

**Promotion signal**: `sdlc-gate-registry-enforcement` merges in both parity repos. That plan's registry
schema, `gate` subcommand surface, and four-repo migration path become this one's foundation —
promote immediately after, while that infrastructure is fresh.
