# Learnings: Optimize the Pull Request Process

- [Repo-grounded] The historic plan-quality gate converged only after commands were routed through
  canonical
  registry surfaces instead of redundant whole-repository scans.
- [Repo-grounded] PLAN Cycle 1 showed the plan itself must obey the human-size rule: foundation and
  idea retirement are clearer as separate sequential PRs.
- [Judgment call] A delivery DAG needs reverse-DAG rollback, collision-safe worktree reuse, amendment
  transactions, and live execution evidence; local-only rollback or stale prose is not auditable.
- [Repo-grounded] The legacy PR #250 review mandated seven disciplines, used `1 of 7` language,
  opened ten initial threads, and drove an oversized rewrite surface.
- [Repo-grounded] The risk-selected PR #250 review ran Cycles 1–4 within its maximum of five and
  reached semantic exit; Cycle 5 was unnecessary.
- [Repo-grounded] A late fix introduced an unqualified `index` ambiguity. The declared docs-only
  Cycle 4 changed strategy and closed it by distinguishing `active-plan index` from `idea index`.
- [Repo-grounded] REQUIREMENTS PR #251 opened 12 findings across Cycles 1–3. Literal trace checks
  could still miss contradictory terminal states; Cycle 4 changed to state simulation, found zero
  further issues, and reached semantic exit without a confirmation Cycle 5.
- [Judgment call] Recovery should name the failed reasoning method as well as the defect family.
  Otherwise “changed strategy” can repeat the same blind spot under a new label.
- [Repo-grounded] DESIGN PR #252 selected logic, governance, and documentation review instead of a
  fixed full panel. Cycle 1 opened eight actionable findings spanning state termination, rollback,
  generated-surface parity, diagram contrast, and the human reading guide; one coherent repair batch
  addressed all eight before the next cycle.
- [Repo-grounded] The first attempt to publish Cycle 1 replies passed Markdown with backticked terms
  through shell interpolation, so GitHub received incomplete prose. Editing the same native comments
  from reviewed JSON payloads and reading them back restored the audit trail before thread resolution.
  PR automation that writes human-facing artifacts should use literal payload files and verify the
  persisted result; a successful API response alone is insufficient evidence.
- [Repo-grounded] DESIGN Cycle 2 changed from discovery to refutation and found four narrower defects.
  The Cycle 1 Codex-mirror repair had overgeneralized three generated subtrees into whole-tree
  prohibitions. Repairs should preserve the authoritative ownership class instead of widening a path
  rule for convenience; a different probe is useful because a coherent fix batch can still introduce
  a new boundary error.
- [Repo-grounded] DESIGN converged in target Cycle 3 with 12 findings and no recovery cycle. A patch
  ID is a fingerprint of changed content. Because a squash merge creates a new commit without the
  reviewed branch's ancestry, matching patch IDs proved the reviewed and landed changes were
  equivalent.
- [Repo-grounded] DESIGN CI was polled more frequently than the repository's two-minute minimum.
  EXECUTION must use the authoritative cadence and retain this as a process defect, even though no
  rate-limit or CI failure occurred.
- [Judgment call] Twenty-five execution findings cannot stay bootcamp-readable in one repair-sized
  PR. Forecast, CORE, WAVES-ENTRY, WAVES-A, WAVES-RULES, and EXECUTION-CLOSURE slices keep mechanics,
  instantiated units, and final evidence independently reviewable while preserving one worktree and
  sequential dependencies.
- [Repo-grounded] The audited CORE draft reached 405 changed lines after essential review repairs,
  crossing the ratified 400-line ceiling. Split forecasting must use the repaired shape, not only
  the first authoring estimate; CORE-ENTRY and CORE-REVIEW preserve cohesion and repair headroom.
- [Repo-grounded] PR #254 merged remotely, but a merge command that also requested branch deletion
  then tried to check out `main`, which another worktree owned. Repository-qualified API-side merge
  and separate, read-back cleanup avoid coupling a valid remote merge to local checkout state.
- [Repo-grounded] PR #255 was marked ready immediately after routing, before its review cycle. It
  was restored to draft; readiness belongs after clean current-head review, resolved threads, and
  green same-head CI. The repaired PR converged in Cycle 3 without an extra confirmation cycle.
- [Repo-grounded] The first broad EXECUTION-WAVES draft reached 350 changed lines while still
  missing baseline-repair, correction/amendment, and per-gate pause tasks. Compressing atomic tasks
  would make progress unauditable, so WAVES-ENTRY, WAVES-A, and WAVES-RULES replace the single slice.
- [Repo-grounded] WAVES-SPLIT Cycle 3 found that correct ownership prose can still coexist with a
  stale allocation-table cell. Its Cycle 4 recovery swept retired terms before independently
  conserving every column total, then reached semantic exit without an unnecessary Cycle 5.

Add final dogfood results, exceptions, measurements, and retained follow-ups before archival.
