# Learnings: Optimize Governance Markdown

Captured during execution; triaged to a permanent home or explicitly discarded at Phase 17 per
the [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md).

## Planning-Phase Learnings

### Harness agent-directory recursion differs per harness

[Web-cited] Claude Code scans `.claude/agents/` **recursively** and derives agent identity from
the `name` frontmatter key, not the path
([docs](https://code.claude.com/docs/en/sub-agents)). OpenCode does **not** — its maintainers
closed the subdirectory feature request as _not planned_
([opencode#6635](https://github.com/anomalyco/opencode/issues/6635)). Cursor's
`.cursor/agents/` behaviour is undocumented in either direction.

**Why it matters**: reorganizing a source directory that has generated mirrors is only safe if
every mirror consumer tolerates the new shape. The generator must flatten.

**Candidate home**: `docs/reference/platform-bindings.md`, or the
[Multi-Harness Binding Convention](../../../repo-governance/conventions/structure/multi-harness-binding.md).

### `parity manifest validate` is repo-local, not cross-repo

[Repo-grounded — `apps/rhino-cli/src/application/parity.rs::validate_at_root`] The gate compares
a repo's committed manifest against that same repo's tracked boundary. It never fetches siblings.
Deferring a rhino-cli change in one of the three repos therefore produces **silent divergence**,
not a red gate.

**Why it matters**: the risk of a partial cross-repo rollout was previously described as
"breakage". It is not. It is undetected drift, which is arguably worse because nothing surfaces it.

**Candidate home**: [Related Repositories reference](../../../docs/reference/related-repositories.md).

### `path-gated` was never exercised on the `ci` surface

[Repo-grounded — `repo-config.yml`, `commands/gate/run.rs`] All six existing `path-gated`
declarations are on `pre-push`. Reading the runner shows the scope is surface-agnostic and CI
changed-paths are computed from `RHINO_GATE_CHANGED_BASE` or `git merge-base origin/main HEAD` —
but no gate had proven it in practice.

**Why it matters**: `candidate_paths` must classify the gate as needing changed paths, otherwise
`changed_paths` is `None` and the skip predicate silently skips **every** run. A gate that never
fires reads as green.

**Candidate home**: the gate-registry documentation in `repo-config.yml`'s header comment.

### `merged_budget_config` merges harness-registry globs, undocumented anywhere else

[Repo-grounded — `instruction_size.rs::merged_budget_config`] The byte-budget gate silently
extends itself with every `harness:` registry entry's `instruction:` glob list, applying
default thresholds to globs with no explicit surface entry. Nothing outside that one function
consumes `harness.instruction` (verified by grep), and none of the four surfaces it would cover
exist in either repo yet. The word-budget gate deliberately drops this behaviour rather than
port it.

**Why it matters**: a "repurpose this module" plan can miss a secondary behaviour that isn't
visible from the primary code path unless the full file is read.

**Candidate home**: `prd.md` FR-1.15 already carries the decision record; no further doc needed.

### Governance-schema `description` was WARN-severity, not FAIL

[Repo-grounded — `frontmatter.rs::validate_governance_schema` vs. `validate_software_schema`]
Only `title` was FAIL for governance docs; `description` used a plain `SEVERITY_WARN`
construction. The software-engineering schema, by contrast, already used `mk_fail()` for both
fields. A first draft of this plan assumed the two schemas already agreed and wrote a Gherkin
scenario claiming software-engineering docs "still only warn" — factually wrong, caught only by
reading `validate_software_schema` directly.

**Why it matters**: assuming two similarly-named validators behave the same without reading both
produces confidently-wrong acceptance criteria.

**Candidate home**: `prd.md` FR-4.2/FR-4.8 already carries the decision record; no further doc needed.

## Execution-Phase Learnings

_Populated during Phases 0-16._

## Discarded

_Observations considered and deliberately not promoted, with the reason._
