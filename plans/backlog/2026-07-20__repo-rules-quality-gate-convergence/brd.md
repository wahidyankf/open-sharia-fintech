# Business Requirements — Repo Rules Quality Gate Convergence

## Business Goal

Make the
[repo-rules-quality-gate workflow](../../../repo-governance/workflows/repo/repo-rules-quality-gate.md)
reach a **trustworthy** zero in materially fewer rounds, with **zero reduction** in the
inconsistencies it catches.

The gate is the only systematic defense against governance text drifting out of agreement with
itself. Governance text is what agents read before acting, so a surviving contradiction does not stay
a documentation defect — it becomes wrong agent behavior at scale, across three repositories. The
goal is therefore strictly cost-side and trust-side: same catch rate, fewer rounds, and a zero that
means something.

## Business Impact

### Pain points (all observed in the archived 2026-07-20 chain)

**Every round found a new blind spot, so no round could be trusted as the last.** Twelve consecutive
corrective commits, each closing a class the previous sweep had structurally missed. The failure was
never "the checker did not look hard enough" — it was "the checker's search shape excluded a region
it did not know existed."

**"Repo-wide" was asserted, not demonstrated.** Commit messages and reports described sweeps as
repo-wide while the sweep never left `repo-governance/`. This is mechanically provable after the
fact: `.github/` and `specs/` were first touched by the twelfth and final corrective commit
[Repo-grounded — `git show --name-only c30ac344e`]. Nothing in the workflow required the sweep's
scope to be stated in a falsifiable form, so nothing caught the gap for eleven rounds.

**The loop's own fixes created new drift.** Round 11 (`362c23aab`) corrected claims that the chain's
own earlier commits had falsified. A loop whose corrective step invalidates its own prior
documentation cannot converge on documentation consistency without an explicit re-check of its own
change surface.

**A false alarm nearly manufactured work inside a byte-identity boundary.** A validator invoked
without CI's flags reported violations that were the validator's own negative fixtures. Acting on it
would have produced a three-repository change chasing a phantom. Nothing in the workflow required an
evidence-producing command to match the command CI actually runs.

**The stated convergence expectation is falsified and still shipped.** The pattern convention says
the loop "should converge in 1-3 iterations" and to "stop and escalate after 5"
[Repo-grounded — `maker-checker-fixer.md` §Preventing Iteration Loops]. The observed chain ran 13.
An expectation that is wrong by a factor of four teaches every future reader to distrust the
document rather than the chain.

### Expected benefits

- **A falsifiable scope claim.** Recording the sweep command verbatim converts "I swept repo-wide"
  from an assertion into a checkable statement.
- **A mechanical detector for the most expensive class.** The never-touched-candidate set is pure
  `git` arithmetic and costs no AI tokens; class 12 alone consumed a full round.
- **Sweeping by a stable key.** Inbound link targets do not paraphrase themselves; prose does.
  [Judgment call] — classes 1, 3 and 4 all follow from keyword-shaped searching, and commit
  `39500d0a2` is the one controlled comparison available, but a single chain is one data point.
- **A zero that survives an adversarial round.** Requiring the checker to argue against its own zero
  before accepting it targets the exact failure the chain exhibited: confident termination on an
  incomplete search.
- **Durable blind-spot memory.** Each class is paid for once, repo-wide, rather than rediscovered.

### Non-benefit — explicitly not a goal

Reducing the number of findings the gate reports. If these changes caused the gate to report fewer
real inconsistencies, the change has failed. Success is _same findings, found earlier, with a
terminal verdict that can be trusted_.

## Affected Roles

Solo-maintainer repo — these are hats the maintainer wears and agents that consume the surfaces.

| Role / consumer             | How this change lands                                                                              |
| --------------------------- | -------------------------------------------------------------------------------------------------- |
| Maintainer running the gate | Gains a bounded budget and a terminal verdict backed by an adversarial round rather than fatigue   |
| `repo-rules-checker`        | Inbound-link sweep becomes primary; sweep transcript required; adversarial round before zero       |
| `repo-rules-fixer`          | Class-wide sweep obligation; must re-check its own change surface for self-inflicted drift         |
| `repo-rules-maker`          | Consumes the BSCR when propagating a rule change, so propagation starts complete rather than local |
| Sibling gate agents         | Inherit the BSCR vocabulary once adopted (DECISION 5)                                              |
| Maintainer reviewing a PR   | Sweep scope is auditable from the report without re-deriving it                                    |
| `ose-primer` / `ose-infra`  | Receive the same registry and validator, keeping the three repos' gates comparable                 |

## Business-Level Success Metrics

Stated as observable checks, not fabricated numbers.

1. **Never-touched detection replays.** Replaying the archived chain's intermediate states through
   the new deterministic pass flags `.github/`, `specs/` and the root-level candidates as
   never-touched at the point where the chain had claimed repo-wide completion. Observable: the
   validator reports a non-zero never-touched count against a fixture reproducing the round-11 state,
   and **zero** against a fixture reproducing the post-`c30ac344e` state. Falsifiable both ways.
2. **Sweep scope is auditable.** An audit or fix report produced by the changed agents contains the
   verbatim sweep command and its exclusion set. Observable by reading the report.
3. **Termination is defined adversarially.** The workflow's termination criteria name the adversarial
   round and the never-touched precondition. Observable by grep against the workflow file.
4. **No check was removed.** The count of validation steps in `repo-rules-checker.md` does not
   decrease. Observable by comparing the Step inventory recorded in Phase 0 against the post-change
   inventory.
5. **Flag-parity guard is live.** A validator invocation cited as evidence either matches CI's flags
   or carries a written divergence justification. Observable by reading the agent contract and by the
   Phase 4 fixture test.

Deliberately not claimed: any specific round-count reduction. [Judgment call] — the mechanisms should
reduce it substantially, but one archived chain is one data point and the honest position is that the
next few chains are the measurement.

## Business-Scope Non-Goals

- Lowering any criticality threshold, or moving any existing finding class below threshold.
- Making the gate advisory rather than blocking.
- Reducing audit report depth or removing the progressive-writing requirement.
- Optimizing the gate for token cost at the expense of catch rate.
- Reworking the sibling repo gates (see DECISION 5) or the plan-quality gate (see DECISION 6).

## Business Risks and Mitigations

| Risk                                                                                            | Mitigation                                                                                                                                      |
| ----------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| **The never-touched set is enormous and unusable** — most repo files are legitimately unrelated | The set is scoped to _candidate_ files: those linking to, or linked from, the changed governing document, plus its declared blast radius (DD-3) |
| **The adversarial round becomes a rubber stamp** — the checker argues against itself pro forma  | The round must consume the mechanical never-touched set as its agenda, not free-form doubt; an empty agenda is itself reported                  |
| **The exclusion-justification requirement invites boilerplate** justifications                  | Exclusions are enumerated as literal globs in the report, so a reviewer sees the actual scope rather than prose about it                        |
| **The BSCR ossifies** — entries added once, never revisited                                     | Every entry carries a git-commit proof that stays checkable; Knowledge Capture obliges appending any newly surfaced class                       |
| **Tri-repo propagation drift** — `ose-primer` / `ose-infra` diverge from `ose-public`           | Byte-identity check for `apps/rhino-cli` per the SDLC Gate Standard; per-repo propagation phases with their own gates                           |
| **Scope creep** — the plan grows to fix every maker-checker-fixer gate                          | Explicitly out of scope; recorded as DECISION 5 with a Knowledge Capture follow-up                                                              |

## Related

Product-level requirements, personas, and the testable Gherkin scenarios for each mechanism live in
[prd.md](./prd.md). Architecture, the BSCR seed content, and design decisions live in
[tech-docs.md](./tech-docs.md).
