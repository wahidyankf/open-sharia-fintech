# The Four Coordination Functions

Once the selected specialists (or, for a `trivial`-tier PR, this agent's own single generalist
pass) emit their raw findings, run exactly four functions over them, in this order, before any
finding is postable:

1. **Deduplicate** — collapse findings from different specialists that name the same `file:line`
   defect into one consolidated thread. Two specialists independently flagging the same line is
   confirmation, not two findings.
2. **Re-categorize** — reassign a misfiled finding to the correct discipline using the
   [boundary tie-breaker rule](../../../../repo-governance/development/quality/pr-review-disciplines/the-boundary-tie-breaker-rule.md#the-boundary-tie-breaker-rule)
   and its
   [seven grey-zone rulings](../../../../repo-governance/development/quality/pr-review-disciplines/seven-grey-zone-rulings.md#seven-grey-zone-rulings).
   This agent **explicitly owns the architecture-versus-correctness boundary** — the highest-risk
   of the three tie-breaker outcomes, because a new structural decision and a domain-behavior
   question can look identical in a raw finding. No specialist self-adjudicates its own
   tie-breaker verdict once this agent has reviewed it.
3. **Reasonableness-filter** — drop speculative, nitpick, false-positive, or
   convention-contradicted findings before they reach the fixer. This is the direct antidote to
   "more agents = more raw findings without more value," and it is also the collective backstop
   for every specialist's own `SUPPRESS` block: a finding that slipped past one specialist's own
   suppression discipline still does not survive this filter.
4. **Tool-verify** — when uncertain about a finding, re-read the cited source (and, if needed,
   delegate to `web-researcher` for anything requiring multi-page research) rather than passing
   an unverified finding through. Never post a finding on the strength of agreement-counting
   alone.

A finding survives all four functions before it is eligible for the consolidated review; a
finding that fails any one of them is dropped, recategorized-and-re-evaluated, or held for
verification — it is never posted "as-is, just in case."

## Attribution Tracking (DD-11), Required for Every Finding

While running the four functions, track which specialist(s) originated each finding — a raw
finding a single specialist raised keeps a single-name byline; a finding two or more specialists
independently raised (a Deduplicate-function merge) keeps every contributing specialist's name,
since multi-specialist convergence on the same root cause is itself a confidence signal worth
surfacing, not collapsing away. Also tally each fanned-out specialist's total raw-finding count
(before dedup/filter), including specialists that fired and found nothing, and specialists the
Content-Type Applicability Filter (DD-10) skipped this cycle and why. This is the sole durable,
per-cycle record of which disciplines earn their fan-out cost — the
[Post-Cutover Monitoring Plan](../../../../repo-governance/development/quality/pr-review-disciplines/post-cutover-monitoring-rollback-monitoring-plan-part-1.md#post-cutover-monitoring-plan)
depends on this data existing somewhere auditable; a posted review missing it is not analyzable
later.
