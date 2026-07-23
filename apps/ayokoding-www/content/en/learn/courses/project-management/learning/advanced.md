---
title: "Advanced Scenarios"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 30
---

Scenarios 19-25 close the topic at the judgment layer: metric abuse, right-sizing process itself,
diagnosing a methodology mismatch, recovering a slipping critical path, turning a retrospective into
tracked change, watching a risk register live across sprints, and finally assembling everything --
WBS, critical path, estimate, sprint plan, risk register, and metrics plan -- into one internally
consistent Aurora delivery plan.

---

### Worked Scenario 19: The Velocity-as-Target Memo

**Context**: Exercises co-14 and co-05. At a different organization, the engineering director for the
Comet team proposes tying part of each team's quarterly bonus multiplier to average story-point
velocity, reasoning that "faster teams should be rewarded." A senior engineer is asked to write the
memo explaining why this backfires before the policy ships.

**Decision artifact**:

> **Memo: why velocity-linked bonuses backfire**
>
> Story points are relative-size estimates a team produces about its own future work (co-05) -- they
> are not an externally measured unit like lines of code or a stopwatch. The instant a team's average
> velocity affects its own bonus, the team gains a direct, rational incentive to inflate its
> estimates: the same PayPal-adapter-sized story that used to be called a 5 gets called an 8, with
> zero change to the actual work. This is Goodhart's Law in its purest form -- the measure becomes
> the target, and stops being a good measure the moment it does.
>
> The damage is not limited to unfairness between teams. It also destroys the number's original,
> legitimate use: once a team's own historical velocity is inflated, that team's own future sprint
> forecasts (co-05) become meaningless too, because they are built on an average that no longer means
> what it used to.
>
> **Proposed alternative**: reward outcome metrics the team does not control the raw units of --
> cycle-time trend (computed independently of any self-report; a team cannot "estimate" its way to a
> shorter cycle time) and defect-escape rate. Neither can be inflated by a team simply agreeing to
> call things bigger.

**Verify**: the memo explains the point-inflation mechanism specifically (same work, bigger declared
number) and proposes a concrete outcome-metric alternative (cycle time, defect-escape rate) --
satisfying co-14's combined rule with co-05.

**Key takeaway**: The fix for Goodhart's Law here is not "stop estimating" -- estimation still serves
forecasting (co-05) perfectly well. The fix is refusing to let that same number double as a
performance signal.

**Why It Matters**: This is not a hypothetical worry -- any measure a team self-reports and that also
affects that team's own outcomes will drift toward whatever number benefits the team, regardless of
intent. The only durable fix is choosing metrics the team does not control the raw units of in the
first place.

---

### Worked Scenario 20: Right-Size Process by Team Size

**Context**: Exercises co-15. Aurora has spun off a two-person spike team prototyping a new feature
alongside the main eight-person delivery team -- and both are currently running the identical fixed
ceremony package (daily standup, biweekly planning, biweekly retro, roughly three hours per person
per week).

**Decision artifact**:

| Team               | Size | Communication paths (`n(n-1)/2`) | Recommendation                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------ | ---- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Spike team         | 2    | 1                                | Drop the formal daily standup and the separate retro ceremony. With exactly one communication path, the two engineers already talk continuously at their two desks -- a 10-minute end-of-week check-in replaces the retro. The fixed ~3 hours/person/week ceremony package would otherwise consume a much larger share of this team's total weekly capacity than it does for a larger team. |
| Main delivery team | 8    | 28                               | Keep the full package: daily standup, biweekly planning, biweekly retro. Twenty-eight communication paths genuinely need synchronization ceremony to prevent silent divergence -- the identical ~3 hours/person/week is a proportionately smaller tax here, buying protection against a much larger coordination surface.                                                                   |

**Verify**: both recommendations cite the team's actual communication-path count (`1` and `28`
respectively, from `n(n-1)/2`) as the basis for how much ceremony is proportionate -- satisfying
co-15's rule.

**Key takeaway**: The identical ceremony package is right-sized for one team and oversized for the
other -- not because of preference, but because the coordination-cost curve the ceremony exists to
manage genuinely differs by team size.

**Why It Matters**: This is the same n(n-1)/2 curve behind Scenario 21's methodology-antipattern
diagnosis: process cost that is roughly flat per person is proportionate on a large team and waste on
a small one, purely because the coordination need it is meant to offset grows quadratically, not
linearly. Trimming ceremony for the two-person team trades a small amount of process uniformity
across the org for hours of working time returned every week.

---

### Worked Scenario 21: Diagnose a Methodology Antipattern

**Context**: Exercises co-02 and co-15. The MedGuard infusion-pump firmware team -- the same regulated
hardware context named in Scenario 2 -- has been running full Scrum ceremony for a year: two-week
sprints, daily standup, and a sprint-review demo with no external stakeholder attending, since there
is no engaged customer able to reprioritize mid-cycle. Regulatory requirements are locked roughly
eight months before code is written.

**Diagnosis**: Scrum's core value is frequent reprioritization with an engaged customer. On this
team, that customer is effectively the regulator, and the regulator does not reprioritize
sprint-to-sprint -- the requirements were locked long before Sprint 1 even started. That means
Scrum's central benefit has no attachment point here, while its full cost (sprint-review prep for a
demo nobody outside the team attends, backlog grooming for a backlog that is not actually
re-orderable against regulatory design controls) is still being paid in full.

**Decision artifact**:

> **Methodology diagnosis -- MedGuard**
>
> - **Mismatch**: Scrum's benefit (fast reprioritization with an engaged, present customer) requires
>   a customer able to reprioritize mid-cycle. MedGuard's actual "customer" is a regulatory design-
>   control process locked roughly eight months before coding starts -- there is no reprioritization
>   to enable, so the benefit is structurally unavailable while the ceremony cost is paid in full.
> - **Better fit**: waterfall-with-milestones, replacing sprints with phase gates tied to the
>   regulatory design-control sequence (design-input freeze, verification, validation, release) --
>   the fixed-scope, high-cost-of-change context Scenario 2 already identified waterfall as fitting.
> - **What survives the switch**: co-08's execution mechanics still add value regardless of
>   methodology -- redesign the daily standup as a blocker-focused check-in (Scenario 17's format),
>   keep it, and drop only the Scrum-specific ceremony that assumed reprioritization capability the
>   team never actually had.

**Verify**: the artifact names the specific mismatch (no reprioritization capability, ceremony cost
paid anyway) and proposes a concrete better fit (waterfall-with-milestones, with the still-useful
execution mechanics kept) -- satisfying the combined co-02/co-15 rule.

**Key takeaway**: The antipattern here is not "Scrum is wrong" in the abstract -- it is Scrum applied
to a context (Scenario 2's regulated-hardware row) that Scenario 2 already flagged as a waterfall
fit, with a year of paid ceremony cost as the receipt.

**Why It Matters**: Cargo-culting a methodology because it is the default at the company, rather than
because it fits the work, is exactly what co-02 warns against -- and this scenario shows the concrete,
measurable cost of getting that fit wrong for an entire year rather than catching it up front. The fix
trades short-term disruption -- retraining a team already comfortable with Scrum's rituals -- for a
full year's worth of ceremony cost recovered every year going forward.

---

### Worked Scenario 22: Crashing vs Fast-Tracking

**Context**: Exercises co-04 and co-01. Midway through the Aurora project, 3.1 (the checkout
end-to-end test suite) runs three days longer than planned because of flaky test infrastructure --
and 3.1 sits on the critical path identified in Scenario 5. The 17-day critical path is now tracking
three days late against the November 15 date, which Scenario 1 already established as fixed.

**Decision artifact**:

> **Recovery options for the Aurora critical path**
>
> - **Crashing** (spends cost): add a second QA engineer, at contractor day rate, to close out 3.1's
>   remaining test cases in parallel. Recovers time by paying for it directly; does not change the
>   risk profile of the work itself.
> - **Fast-tracking** (spends risk): start 3.2's environment setup and initial load-test ramp in
>   parallel with 3.1's final regression pass, instead of strictly waiting for 3.1 to finish first.
>   Recovers time by overlapping normally sequential work; accepts the risk that the load test begins
>   against a not-yet-fully-validated build, and might surface an integration bug the completed E2E
>   pass would otherwise have caught first.
>
> **Decision**: a blended recovery. Fast-track two of the three needed days (overlap 3.2's setup and
> initial ramp with 3.1's tail end); crash the remaining one day (add a second QA engineer for one
> day to close out 3.1's last test cases faster). This recovers all three days without moving the
> fixed November 15 date or cutting scope -- consistent with Scenario 1's original trade-off.

**Verify**: each option is explicitly tied to the constraint it spends -- crashing to cost, fast-
tracking to risk -- and the final blended decision states exactly how many days each option
recovers, satisfying the combined co-04/co-01 rule.

**Key takeaway**: "Add people" (crashing) and "overlap sequential work" (fast-tracking) are not
interchangeable recovery moves -- one spends money, the other spends risk, and a real recovery plan
should say which one it is choosing and why.

**Why It Matters**: This is co-01's triangle again, at a smaller scale and mid-project instead of at
kickoff: the fixed date from Scenario 1 has not moved, so the three recovered days have to come from
somewhere, and naming exactly where -- one day of cost, two days of accepted risk -- keeps this
recovery a chosen trade instead of a silent one.

---

### Worked Scenario 23: Retrospective to Tracked Actions

**Context**: Exercises co-12. Aurora's Sprint 2 retrospective produces four raw observations: "the
deploy pipeline broke twice," "nobody noticed the staging outage for a day" (the same outage
diagnosed in Scenario 11), "pairing on the cart-persistence code helped a lot," and "planning poker
took too long because half the team wasn't prepared."

**Decision artifact**:

| #   | Raw observation                                                     | Tracked action                                                                                                             | Owner | Done-signal                                                                                                                |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | Nobody noticed the staging outage for a day.                        | Add a staging-environment health check as a standing standup item (Scenario 11's corrective action, now made permanent).   | Priya | Appears as a standing standup line item, confirmed present for two consecutive sprints.                                    |
| 2   | The deploy pipeline broke twice.                                    | Add an automated smoke test as the first stage of the deploy pipeline, so breakage is caught before reaching later stages. | Bayu  | The pipeline dashboard shows the new smoke-test stage green on the next three consecutive deploys.                         |
| 3   | Pairing on the cart-persistence code helped a lot.                  | Continue pairing specifically for any story touching legacy cart-persistence code (not team-wide pairing).                 | PM    | The next legacy-touching backlog story is explicitly paired, confirmed on the sprint board.                                |
| 4   | Planning poker took too long because half the team wasn't prepared. | Send a standing "read these stories before the session" note the day before every planning-poker session.                  | PM    | The next session finishes in 30 minutes or less for a similarly sized slice (baseline: the prior session took 55 minutes). |

**Verify**: every one of the four actions has a named owner and a measurable done-signal (something
checkable next sprint, not a vague intention) -- satisfying co-12's rule.

**Key takeaway**: Four raw complaints became four owned actions with a concrete way to check, next
sprint, whether each one actually happened.

**Why It Matters**: Action #1 shows retrospectives and metrics diagnosis (Scenario 11) working
together directly -- the corrective action first proposed as a one-time fix for a specific burndown
flatline becomes, through the retrospective, a permanent process change instead of something the team
has to rediscover the next time an environment outage happens.

---

### Worked Scenario 24: Risk Register Over Time

**Context**: Exercises co-10 and co-12. Scenario 14's risk register is not a one-time document -- it
evolves across three sprints as mitigations land, risk windows pass, and new risks emerge.

**Decision artifact**:

| Risk                                             | Sprint 1                                | Sprint 2                                                                                                     | Sprint 3                                                                                                   |
| ------------------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Apple Pay API breaking change (score 12)         | Open, mitigation in progress.           | Still open.                                                                                                  | **Retired** -- launch week passed safely; the pinned SDK version held.                                     |
| Load test cannot sustain 3x traffic (score 15)   | Open, mitigation scheduled.             | Downgraded to score 9 (impact 5 -> 3) after an early load-test dry run showed better-than-expected headroom. | Retired -- final load test passed at 3.4x peak traffic.                                                    |
| Bayu on scheduled leave (score 15)               | Open, walkthrough scheduled.            | **Retired** -- the walkthrough and runbook mitigation landed before leave started.                           | (Already retired.)                                                                                         |
| Holiday code-freeze shortens schedule (score 12) | Open.                                   | Still open.                                                                                                  | **Retired** -- the freeze date passed without incident; launch shipped ahead of the freeze window.         |
| Finance requests a 6th provider (score 9)        | Open, routed through change management. | Still open (Scenario 16's decision pending finalization).                                                    | Retired -- Scenario 16's formal defer-to-Q1 decision closed the open question.                             |
| Feature-flag rollback bug during 3.3 (new)       | -- not yet identified --                | **New**: discovered during rollout-plan implementation. Score 8 (likelihood 2, impact 4). Owner: Priya.      | Downgraded to score 3 after a partial fix landed; tracked into the Q1 follow-up work alongside Google Pay. |

Full artifact: **[`learning/artifacts/ex-24-risk-register-over-time.md`](./artifacts/ex-24-risk-register-over-time.md)**.

**Verify**: the artifact shows risks explicitly retired as their mitigations land (three risks retired
by Sprint 2-3) and a new risk added as it emerges (the feature-flag rollback bug, first appearing in
Sprint 2) -- satisfying the combined co-10/co-12 rule.

**Key takeaway**: By Sprint 3, four of the original five risks are retired and one new risk has
emerged and is already trending down -- a register that is still being actively worked, not a
document written once at kickoff and never revisited.

**Why It Matters**: A risk register that never changes after Sprint 1 is not evidence that nothing
went wrong -- it is usually evidence that nobody is looking at it anymore. Watching this one evolve
is what makes "living document" (co-10) a checkable claim instead of a slogan. Revisiting the
register every sprint costs a few minutes of standing-meeting time, a trade-off co-10 treats as
strictly cheaper than the alternative: a retired risk quietly re-emerging unnoticed because no one
checked.

---

### Worked Scenario 25: Full Delivery Plan

**Context**: Exercises co-01, co-03, co-04, co-05, co-07, co-09, and co-10. This scenario assembles
every artifact this topic built for the Aurora Checkout Redesign -- the WBS, the critical path, the
velocity estimate, the sprint plan, the risk register, and a metrics plan -- into one internally
consistent delivery plan, the same synthesis the capstone repeats at a larger scale for a different
project.

**Decision artifact**: **[`learning/artifacts/ex-25-full-delivery-plan.md`](./artifacts/ex-25-full-delivery-plan.md)** -- the complete,
standalone plan. In summary:

- **WBS** (Scenario 3): 3 branches, 9 independently estimable and assignable leaves.
- **Critical path** (Scenario 5): 2.1 -> 2.2 -> 3.1 -> 3.2 -> 3.3, 17 working days, zero slack --
  this is the number that drives the November 15 date, not any single payment-adapter branch.
- **Velocity estimate** (Scenarios 6-7): 41 points, 15-point average velocity (from three sprints:
  14, 17, 15), forecasting 3 sprints.
- **Sprint plan** (Scenario 9, extended): Sprint 1 (13 pts: cart persistence, PayPal adapter),
  Sprint 2 (13 pts: Stripe and Apple Pay adapters, order-summary UI, confirmation email), Sprint 3
  (15 pts: E2E suite, load test, rollout plan) -- exactly matching the 3-sprint forecast, with every
  task's dependencies satisfied by an earlier sprint.
- **Risk register** (Scenario 14, current snapshot): 5 risks scored, mitigated, and owned; top three
  by score (Scenario 15) actively worked.
- **Metrics plan**: burndown per sprint (flatline for 2+ days -> investigate a blocker same day, per
  Scenario 8 and confirmed live in Scenario 11); cycle time on the E2E-suite stage specifically
  (trending up for 2 consecutive weeks -> add QA capacity or lower that stage's WIP limit, the same
  diagnostic Scenario 13 applied to Helios's Code Review stage).

**Verify**: the critical path (17 days) drives the schedule commitment, not any individual branch;
the 3-sprint estimate aligns exactly with the 3-sprint plan; and every metric in the metrics plan
names a concrete decision -- satisfying the full combined rule across all seven cited concepts.

**Key takeaway**: None of these six pieces was invented for this scenario -- every number here traces
back to an earlier scenario in this topic, and the only new work is showing they are mutually
consistent when assembled into one document.

**Why It Matters**: A delivery plan that is internally inconsistent -- a sprint plan that doesn't add
up to the velocity forecast, a risk register nobody has touched since kickoff, a metric with no
decision attached -- is a plan in name only. This is exactly the bar the capstone's larger Nimbus
Notification Service delivery plan has to clear next.

---

← Previous: [Intermediate Scenarios](./intermediate.md) · Next: [Capstone](./capstone/overview.md) →
