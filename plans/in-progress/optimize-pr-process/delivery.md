# Delivery Plan: Optimize the Pull Request Process

## Current Execution State

- [x] Formal plan-quality gate passed with two consecutive zero-finding audits.
- [x] Phase 0 installed dependencies, ran doctor, verified both repository baselines, and confirmed
      one owned plan worktree per repository.
- [x] PLAN was committed as `0cab552424994e34d724ad4881793ce3f1941600`, pushed, and opened as
      draft [PR #250](https://github.com/wahidyankf/ose-public/pull/250).
- [ ] PLAN Cycle 1 review/fix is in progress; merge and worktree resync remain pending.

## How a Large Plan Is Made and Executed

1. Capture requirements, research, design, acceptance criteria, delivery DAG, validation, rollback,
   knowledge capture, and closure in the six plan documents before implementation.
2. Run `repo-governance/workflows/plan/plan-quality-gate.md`; amend the plan until its semantic exit
   passes. Read every external source listed in README.md; that list is the single source of truth.
3. After explicit execution authority, run `repo-governance/workflows/plan/plan-execution.md` from
   the same named worktree in each repository. Plan docs, idea retirement, durable repo rules,
   generated bindings, code/tests, and closure are separate bounded delivery concerns.
4. Split work that exceeds 400 changed hand-authored lines, 20 hand-authored files, or one human
   concern. Use sequential PRs from current `origin/main`; do not stack dependent PRs.
5. End with cross-repo verification, process dogfood, `learnings.md`, execution checking, plan
   archival, exact owned-worktree cleanup, and proof that both `origin/main` branches contain results.

## Worktree and Branch Transition

Use only `/Users/wkf/ose-projects/ose-public/worktrees/optimize-pr-process` and
`/Users/wkf/ose-projects/ose-private/worktrees/optimize-pr-process`. Before a new unit, prove the
worktree clean, fetch `origin`, and inspect the proposed fixed branch name. Create the branch from
current `origin/main` only when absent. If it exists, prove it fully merged and safely deletable;
otherwise stop and record the unique commits and recovery options. Never force-reset a branch name.

After each merge, fetch, read the full landed diff, verify clean status and ancestry, align the same
worktree to `origin/main`, then start the next dependency. Cleanup removes only these exact two owned
worktree paths after all work is merged; a read-only worktree listing proves removal. Do not perform
repository-wide worktree housekeeping.

## Sequential Delivery Units

| Unit             | Concern and integration safety                                                                  |
| ---------------- | ----------------------------------------------------------------------------------------------- |
| PLAN             | Concise control plan only; dormant documentation.                                               |
| PUB-IDEAS        | Public idea retirement/index/link cleanup only, mapped to merged PLAN.                          |
| PRIV-IDEAS       | Private idea retirement/index cleanup only, pinned to merged PLAN and PUB-IDEAS.                |
| PUB-A1 → PRIV-A1 | Human-readable PR body, size, atomicity, reading guide; ordered rule activation.                |
| PUB-A2 → PRIV-A2 | Teaching findings, native replies, dispositions, audit trail, AI marker; compatibility bridge.  |
| PUB-A3 → PRIV-A3 | Scope freeze, readiness, cycles 1–3 target, Cycle 5 ceiling, exit and escalation.               |
| PUB-B → PRIV-B   | Planning, one-worktree lifecycle, delivery, knowledge, archival, cleanup, bindings.             |
| PUB-C? → PRIV-C? | Existing CI repair only if the mechanism-necessity evidence passes; otherwise no-change record. |
| closure          | Cross-repo dogfood, learnings, execution audit, final public archival.                          |

Every public rule unit invokes
`repo-governance/workflows/repo/repo-rules-propagation.md` in the public worktree, records normalized
rules and enforcement dispositions, regenerates bindings, and opens a private sibling obligation.
The private unit starts only from the exact merged-green public PR/SHA and records semantic parity,
repo-specific deviation, or byte-identity handling under the affected surface authority.

## Repeatable Unit Transaction

- [ ] Prove dependency pins, clean status, one owned worktree, stable `main`, exact scope, size, and
      the lightest-fit “feature flag”; stop on branch collision or incoherent scope.
- [ ] Edit only the unit ledger. For repo rules, use the canonical propagation workflow rather than
      manual cross-repo copying; generate harness bindings from `.claude/` sources.
- [ ] Stage explicit paths, run the staged pre-commit registry surface, and reconcile the cache
      exactly. Inspect the complete staged diff before the conventional commit.
- [ ] Run post-commit pre-push registry gates and affected targets. Push normally and open exactly
      one draft PR; keep it draft through review/fix convergence.
- [ ] Give the PR a concise human reading guide, verification, dependency/obligation, integration
      safety, stable-main proof, rollback, diagram decision, and `Generated by AI` footer.
- [ ] Run risk-based review, one consolidated review, same-thread four-way fixer replies, and CI on
      the current head. Resolve only addressed threads; never absorb unrelated work.
- [ ] Mark ready and merge only after semantic exit, then record merge SHA, read the landed diff,
      resync the worktree, and discharge or carry forward the native obligation.

## Cross-Repository Recovery and Rollback

Classify private discoveries as `private-only`, `repo-specific deviation`, `portable source defect`,
or `byte-identity`. The first two stay private. A portable defect stops private delivery and permits
one public correction PR for that wave; pin the old/new source and close any opened private PR as
linked `superseded` before one replacement. A second upstream correction or reversal is oscillation:
stop, preserve stable `main`, and escalate with options. No terminal unrelated wave is reopened.

Rollback follows the reverse DAG. Unwind merged dependents before their source, private then public
within a pair. While a pair is temporarily incoherent, its PR thread records pins, status, owner,
next action, and whether repair or revert is active. Finish only when both repositories are green
and the obligation is resolved by native evidence.

## Remaining Phases

- [ ] Merge/resync PLAN, then deliver PUB-IDEAS and PRIV-IDEAS as separate PRs.
- [ ] Phase 3: freeze scope and evidence read-only. If tracked plan text must change, stop and run a
      complete `PLAN-AMENDMENT` branch → gates → draft PR → review → CI → merge → resync transaction.
- [ ] Deliver paired A1, A2, A3, and B waves in DAG order; assess optional C without default tooling.
- [ ] Reconcile every public/private pin and open obligation; dogfood the resulting PR process.
- [ ] Capture learnings, run the plan-execution checker, close private work, archive publicly, prove
      both results on `origin/main`, remove only owned worktrees, and focus public `main`.

## Gate Commands

Before commit, stage exact paths and run
`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-commit`; inspect any formatter mutation,
then reconcile `git diff --cached --name-only`. After commit, run `npm run validate:sync`,
`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`, and affected Nx targets when the
unit changes registered projects. Never bypass a failure or widen scope to unrelated baseline debt.
