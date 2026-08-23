# Learnings: Optimize the Pull Request Process

- The plan-quality gate converged only after validation commands were routed through canonical
  registry surfaces instead of redundant whole-repository scans.
- PLAN Cycle 1 showed the plan itself must obey the human-size rule: control-plan establishment and
  idea retirement are clearer as separate sequential PRs.
- A delivery DAG needs reverse-DAG rollback, collision-safe worktree reuse, explicit amendment
  transactions, and live execution evidence; local-only rollback or stale prose is not auditable.

Add final dogfood results, exceptions, measurements, and retained follow-ups before archival.
