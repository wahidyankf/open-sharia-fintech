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

Add final dogfood results, exceptions, measurements, and retained follow-ups before archival.
