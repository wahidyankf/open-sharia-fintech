---
title: "Intermediate Scenarios"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 20
---

Scenarios 9-18 move from framing and scheduling into running the project day to day: turning an
estimated backlog into sprints, keeping estimation honest, reading what the metrics are actually
saying, managing risk as a living document, handling a mid-project scope change, and tailoring
communication to the audience that needs it. Several continue the Aurora Checkout Redesign thread
from the Beginner scenarios; a few introduce the Helios platform team for variety.

---

### Worked Scenario 9: Sprint and Backlog Plan

**Context**: Exercises co-07. With the 41-point Aurora backlog (Scenario 6) and its 15-point average
velocity (Scenario 7) in hand, the team plans its first two sprints -- the payment-adapter and
cart-persistence phase of the project -- respecting both capacity and dependency order.

**Decision artifact**:

| Sprint   | Committed items                                                                                               | Points | Dependency check                                                                         |
| -------- | ------------------------------------------------------------------------------------------------------------- | ------ | ---------------------------------------------------------------------------------------- |
| Sprint 1 | 2.1 Cart persistence rework (8), 1.2 PayPal adapter (5)                                                       | 13     | Neither item has an unmet prerequisite.                                                  |
| Sprint 2 | 1.1 Stripe adapter (5), 1.3 Apple Pay adapter (3), 2.2 Order summary UI (3), 2.3 Order confirmation email (2) | 13     | 2.2 and 2.3 depend on 2.1, which finished in Sprint 1; 1.1 and 1.3 have no prerequisite. |

Neither sprint exceeds the 15-point velocity ceiling. The remaining backlog -- 3.1 E2E suite (8), 3.2
load test (5), 3.3 rollout plan (2), 15 points -- is exactly Scenario 7's third forecast sprint, held
back here because none of it is eligible yet: all three depend on the payment adapters and the
order-summary UI finishing first.

**Verify**: no sprint's committed points exceed the 15-point velocity ceiling, and no committed task
precedes a dependency that is not itself scheduled in an earlier sprint -- satisfying co-07's rule.

**Key takeaway**: Two sprints, 13 points each, both under the 15-point ceiling and both
dependency-clean -- with the third sprint's scope already implied by what is left.

**Why It Matters**: A plan that instead pulled 3.1 into Sprint 1 "to get ahead" would have looked
productive on the sprint board while actually being unstartable -- the E2E suite has no payment
adapters or order-summary UI to test against yet. Respecting dependency order here is what keeps the
sprint board honest.

---

### Worked Scenario 10: Planning-Poker Debiasing Rules

**Context**: Exercises co-06. A newly formed team's planning-poker sessions keep converging on
whatever the tech lead says first -- a textbook case of both anchoring and authority bias operating
at once. The team writes facilitation rules that name and counter each one.

**Decision artifact**:

| Rule                                                                                                                                                                                                      | Bias it neutralizes | How                                                                                                                                                                 |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Blind reveal: every participant privately selects a card; all reveal simultaneously on a countdown.                                                                                                       | Anchoring           | No one's spoken number can pull anyone else's guess before their own is locked in.                                                                                  |
| Outlier discussion before re-vote: when the highest and lowest estimate differ by more than one Fibonacci step, the highest and lowest estimators explain their reasoning first, then the group re-votes. | Authority bias      | The most senior person's number is treated as one estimate to explain, not an automatic answer -- and it is the _outliers_, not the loudest voice, who speak first. |
| Quietest-first: when discussion is needed, the facilitator asks the most junior or quietest team member to explain their reasoning before anyone more senior speaks.                                      | Authority bias      | Prevents the discussion itself from anchoring around whoever is used to speaking first.                                                                             |

**Verify**: each rule names, specifically, which bias (anchoring or authority bias) it neutralizes
and how -- satisfying co-06's rule.

**Key takeaway**: Three small procedural rules -- reveal order, who explains first, who speaks first
in discussion -- are enough to recover the team's real, disaggregated judgment instead of the tech
lead's judgment wearing the team's name.

**Why It Matters**: A team that skips these rules is not actually running planning poker -- it is
running a vote that happens to use poker cards. The rules only work if they are followed every
session, not invoked occasionally when someone notices the anchoring happening. That discipline costs
a few extra minutes of meeting time per session, a small, worthwhile trade against the alternative of
quietly re-litigating the same estimate every time reality proves the loudest voice wrong.

---

### Worked Scenario 11: Diagnose a Flatlined Burndown

**Context**: Exercises co-09. Aurora's Sprint 2 burndown chart drops steadily through day 4, then
flatlines completely from day 5 through day 7 of the ten-day sprint, before resuming its drop on day 8.

**Decision artifact**:

| Day | Remaining points | Note                                                             |
| --- | ---------------- | ---------------------------------------------------------------- |
| 4   | 8                | On pace.                                                         |
| 5   | 8                | Flatline begins.                                                 |
| 6   | 8                | Flatline continues.                                              |
| 7   | 8                | Flatline continues -- three full days with zero progress logged. |
| 8   | 5                | Resumes dropping.                                                |

**Diagnosis**: the shared staging environment was down for two of the three flatlined days, waiting
on a security patch from the platform team. Nobody raised it in standup, because no individual
story was "blocked" in the traditional sense yet -- the outage only became obviously
story-blocking once someone actually needed to deploy and test against staging on day 6.

**Corrective action**: add "is the staging environment healthy" as a standing standup check-in item
(not just "any blockers"), and escalate infrastructure issues within four working hours of
discovery instead of waiting for them to visibly block a specific story.

**Verify**: the artifact names a plausible cause (the staging-environment outage) and one concrete
corrective action (a standing standup health check plus a four-hour escalation window) --
satisfying co-09's rule.

**Key takeaway**: A three-day flatline is rarely "the team is stuck on hard work" -- it is almost
always something environmental going unreported because no single story felt blocked enough to
mention.

**Why It Matters**: This is the same lesson Scenario 23's retrospective turns into a permanent action
-- catching an environment problem on day 5 instead of day 7 recovers two full days of a ten-day
sprint, which is exactly the kind of early-discovery payoff co-08's execution mechanics exist to
produce. A standup that only recites yesterday's status instead of surfacing blockers (co-08) would
have let this same flatline run for the full two weeks before anyone asked why.

---

### Worked Scenario 12: Burnup vs Burndown

**Context**: Exercises co-09 and co-11. With Finance's Google Pay scope request (Scenario 16) under
active discussion, Aurora's stakeholder wants ongoing visibility into project scope -- and a plain
burndown chart cannot show that honestly.

**Reasoning**: a burndown chart plots only remaining work. If a scope change is accepted mid-project,
remaining work jumps back up -- and on a burndown chart, that jump is visually indistinguishable from
the team simply falling behind. A burnup chart instead plots two separate lines: completed work and
total scope. If total scope steps up because a change was accepted, the chart shows that step
explicitly, separate from the completed-work line, so a stakeholder can see "scope grew" without it
looking like "the team got slower."

**Decision artifact**:

> **Recommendation to the Aurora stakeholder group**: switch the shared status chart from burndown to
> burnup for the remainder of the project. Burnup's two-line format (completed work vs. total scope)
> makes any accepted scope change visible as its own event on the total-scope line, rather than
> disguising it as an apparent drop in team velocity on a single remaining-work line.

**Verify**: the rationale explicitly ties scope-change visibility to burnup's separate scope line --
satisfying the combined co-09/co-11 rule.

**Key takeaway**: Burndown and burnup answer the same underlying question (how much is left), but
only burnup keeps "scope changed" and "the team fell behind" visually distinct.

**Why It Matters**: The choice of chart is itself a change-management decision (co-11) -- a burndown
chart quietly makes every accepted scope change look like a schedule failure, which discourages
teams from being honest about scope changes and stakeholders from trusting the chart at all.
Switching charts mid-project costs a brief reorientation for stakeholders used to reading a burndown,
a small one-time cost against months of chronically misread, every-scope-change-looks-like-slippage
status updates.

---

### Worked Scenario 13: Cycle-Time Bottleneck Diagnosis

**Context**: Exercises co-09 and co-08. The Helios platform team's cumulative-flow diagram shows the
"Code Review" column's band widening steadily over two weeks, while "In Progress" and "Done" stay
roughly flat.

**Decision artifact**:

| Workflow stage | WIP, week 1 | WIP, week 2 | WIP, week 3 | Trend   |
| -------------- | ----------- | ----------- | ----------- | ------- |
| In Progress    | 4           | 5           | 4           | Flat    |
| Code Review    | 3           | 6           | 9           | Growing |
| Done           | 12          | 13          | 12          | Flat    |

A widening band on a cumulative-flow diagram, with the stages on either side flat, is the signature
of a bottleneck at that one stage: work is entering Code Review at roughly the same rate it always
has, but leaving it more slowly, so items pile up there instead of moving through.

**Verify**: the artifact identifies Code Review specifically as the stage with growing WIP, backed
by the three-week trend showing the other two stages flat -- satisfying the combined co-09/co-08
rule.

**Key takeaway**: The bottleneck is Code Review, not "the team in general" -- the flat stages on
either side of it are exactly what rules out a team-wide slowdown.

**Why It Matters**: Diagnosing the correct stage matters because the fix is stage-specific: adding a
second reviewer rotation or capping Code Review's WIP limit at 3 addresses this bottleneck directly,
while a team-wide fix (more standups, more planning) would spend effort on stages that were never the
problem. Capping the WIP limit trades a small amount of individual reviewer flexibility for a
system-wide guarantee that no single stage silently absorbs every other stage's slack.

---

### Worked Scenario 14: Build a Risk Register

**Context**: Exercises co-10. With the Aurora schedule (Scenario 5) and backlog (Scenario 6) in
place, the team identifies five risks and records each with a likelihood x impact score, a concrete
mitigation, and a named owner.

**Decision artifact**:

| #   | Risk                                                                                                      | Likelihood (1-5) | Impact (1-5) | Score | Mitigation                                                                                                                                        | Owner                 |
| --- | --------------------------------------------------------------------------------------------------------- | ---------------- | ------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Apple Pay API introduces a breaking change before launch                                                  | 3                | 4            | 12    | Pin the SDK version, subscribe to Apple's developer changelog, smoke-test weekly against the sandbox.                                             | Dinar (payments lead) |
| 2   | Load test reveals checkout cannot sustain 3x peak traffic                                                 | 3                | 5            | 15    | Run the load test three weeks before launch (not launch week), reserve autoscaling headroom, keep a feature-flag kill switch to the old checkout. | Priya (SRE)           |
| 3   | Bayu, the only engineer who knows the legacy cart-persistence code, is on scheduled leave during Sprint 2 | 5                | 3            | 15    | Pair a full walkthrough session before leave starts, document cart-persistence quirks in a runbook.                                               | Bayu (tech lead)      |
| 4   | Holiday code-freeze policy shortens the usable schedule by one week                                       | 4                | 3            | 12    | Confirm the exact freeze date with release management now, and build the week into the schedule buffer rather than discovering it late.           | Dinar                 |
| 5   | Finance requests a sixth payment provider mid-project (scope creep)                                       | 3                | 3            | 9     | Route any such request through the change-management decision process (co-11) rather than silently absorbing it.                                  | PM (Aurora)           |

Full artifact: **[`learning/artifacts/ex-14-risk-register.md`](./artifacts/ex-14-risk-register.md)**.

**Verify**: every one of the five risks has a computed likelihood x impact score, a mitigation
specific enough to act on (not "monitor closely"), and a named owner -- satisfying co-10's rule.

**Key takeaway**: The two highest-scored risks (load-test failure and the key-engineer leave, both 15) are not the ones that "feel" scariest at first glance -- they are the ones the numbers actually
rank highest, which is the entire point of scoring instead of guessing.

**Why It Matters**: Risk #3's mitigation (documenting Bayu's tacit knowledge) is a direct hedge
against the classic single-point-of-failure problem -- the mitigation genuinely reduces the risk
(the team can now operate without Bayu for a week), rather than merely acknowledging it exists.
Naming a single owner per risk trades the comfort of shared, diffuse responsibility for the far more
useful guarantee that someone is actually accountable for the mitigation landing.

---

### Worked Scenario 15: Prioritize Risks by Likelihood and Impact

**Context**: Exercises co-10. With Scenario 14's five scored risks in hand, the team picks the top
three to actively work mitigations for this sprint, rather than treating all five as equally urgent.

**Decision artifact**:

| Rank | Risk                                                   | Score | Rationale for this rank                                                                                                                                                                                         |
| ---- | ------------------------------------------------------ | ----- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Load test reveals checkout cannot sustain 3x traffic   | 15    | Highest impact (5) of any risk -- a launch-blocking failure discovered late.                                                                                                                                    |
| 2    | Key engineer (Bayu) on scheduled leave during Sprint 2 | 15    | Tied on score, but the leave date is fixed and near-term, so its mitigation window is the tightest of any risk on the list.                                                                                     |
| 3    | Apple Pay API breaking change before launch            | 12    | Tied with risk #4 at 12; ranked above it because a third-party API change is outside the team's control entirely, while the code-freeze date (risk #4) is knowable in advance with one confirming conversation. |

**Verify**: the ranking is consistent with the computed scores -- both score-15 risks rank above both
score-12 risks, and the tie-break rationale (mitigation-window tightness, degree of the team's
control) is stated explicitly for both ties -- satisfying co-10's rule.

**Key takeaway**: Prioritizing by score, with explicit tie-break reasoning, is what keeps "which risk
do we work on first" from becoming a gut-feel argument.

**Why It Matters**: The two risks that did not make the top three (the holiday freeze and the
scope-creep risk) are not ignored -- they stay on the register with their existing mitigations
already assigned, simply without dedicated attention this sprint. Scenario 24 revisits this exact
register two sprints later to show how it evolves.

---

### Worked Scenario 16: Change-Request Decision

**Context**: Exercises co-11 and co-01. Mid-Sprint-2, Finance formally asks Aurora to add a sixth
payment provider, Google Pay, to the current scope -- exactly the scenario risk #5 (Scenario 14)
already anticipated.

**Reasoning**: the launch date and the original core scope are already fixed (Scenario 1), and the
budget for the three-provider contractor expansion is already committed and fully allocated.
Accepting Google Pay into the current scope would require either moving the date, cutting an
already-committed feature, or adding budget beyond what Finance itself approved -- none of which
Finance is asking for. The team routes the request through its change-management process (exactly
as risk #5's mitigation specified) rather than quietly saying yes.

**Decision artifact**:

> **Change-request decision -- Google Pay addition**
>
> - **Decision**: Defer. Google Pay is not added to the current Aurora scope.
> - **What is absorbed**: nothing is added now; Google Pay becomes a committed Q1 fast-follow item,
>   tracked and scheduled immediately after launch, so it is communicated to stakeholders as
>   "coming next," not "dropped."
> - **Why not accept-and-trade**: accepting it into current scope would require either the fixed
>   November 15 date to move, an already-committed provider (Stripe, PayPal, or Apple Pay) to be
>   cut, or budget beyond what Finance itself approved for the contractor expansion -- none of which
>   the request itself asked for.

**Verify**: the decision states explicitly what would have to be dropped, delayed, or funded to
accommodate the change, and lands on "defer, with a committed follow-up date," rather than a bare
"approved" or "denied" -- satisfying co-11's rule.

**Key takeaway**: "Defer to next quarter, committed and scheduled" is a real accept/defer/trade
decision -- it is not the same as silently ignoring the request or bluntly refusing it.

**Why It Matters**: Because risk #5 already named this exact scenario with a mitigation in place, the
team was not caught off guard -- the risk register (co-10) and change management (co-11) worked
together here exactly as designed: anticipate the pressure, then handle it through the process built
for it. Deferring instead of silently absorbing the request trades a disappointed stakeholder today
for a schedule and budget that still mean what they said at kickoff.

---

### Worked Scenario 17: Redesign a Status-Theater Standup

**Context**: Exercises co-08. The Helios platform team's daily standup runs 25 minutes: each person
recites what they did yesterday, what they'll do today, and says "no blockers" -- and blockers
routinely surface two or three days later anyway, once someone finally asks why a card hasn't moved.

**Decision artifact**:

|                    | Before (status-theater)                                   | After (blocker-and-board-focused)                                                               |
| ------------------ | --------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Structure          | Round-robin: each person speaks in turn about themselves. | Walk the Kanban board right-to-left, closest-to-done first; speak only when your card comes up. |
| Mandatory prompts  | "What did you do yesterday? What will you do today?"      | "Is this card blocked?" and "Has this card been sitting longer than two days?"                  |
| Typical length     | 25 minutes                                                | Under 10 minutes -- most cards get a silent "on track," only flagged cards get discussion.      |
| What gets surfaced | Individual activity, rarely a blocker.                    | Blockers and aging WIP, directly and consistently.                                              |

**Verify**: the redesigned format structurally surfaces blockers and WIP (two mandatory prompts, per
card, board-driven) rather than a chronological personal status report -- satisfying co-08's rule.

**Key takeaway**: Walking the board and asking two fixed questions per card produces more real signal
in less time than a personal status round-robin ever did.

**Why It Matters**: The old format asked people to self-report blockers, which requires someone to
first recognize their situation _as_ a blocker worth mentioning. The new format asks the same two
questions of every card regardless of who owns it, which catches the "I didn't realize this counted
as blocked" cases the old format structurally missed.

---

### Worked Scenario 18: Stakeholder Communication Plan

**Context**: Exercises co-13. Aurora has four genuinely different audiences, each needing a different
cadence, format, and depth -- and each update needs to drive a real decision, not just report status.

**Decision artifact**:

| Audience                              | Cadence                                          | Format                                                    | Decision it drives                                                                                                       |
| ------------------------------------- | ------------------------------------------------ | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Executive sponsor                     | Monthly                                          | One-page memo (date, budget, and risk status).            | Fund a mitigation, or accept a date-risk trade-off.                                                                      |
| Product stakeholder (Finance liaison) | Every sprint review (biweekly)                   | Live demo plus the burnup chart (Scenario 12).            | Reprioritize the backlog, or decide on a scope request like the Google Pay ask (Scenario 16).                            |
| Downstream fraud and risk team        | Two weeks before each payment provider goes live | Written interface-change notice with a test-sandbox link. | Approve provider-specific fraud rules before that provider's rollout.                                                    |
| Engineering-wide (other teams)        | Async, on milestone completion only              | A short digest post.                                      | Other teams decide whether their own dependent work can now safely integrate against the new payment-adapter interfaces. |

**Verify**: every audience row names the specific decision the update is meant to drive, not merely
the information the update contains -- satisfying co-13's rule.

**Key takeaway**: Even the lowest-cadence audience row (engineering-wide, milestone-only) still names
a real decision -- "can we integrate now" -- rather than being pure information-for-its-own-sake.

**Why It Matters**: A stakeholder who gets the sponsor's monthly one-pager on a weekly cadence tunes
out from over-frequency; a downstream team that only hears about an interface change after it ships
gets blindsided. Matching cadence and depth to each audience's actual decision is what keeps every
one of these four channels worth reading.

---

← Previous: [Beginner Scenarios](./beginner.md) · Next: [Advanced Scenarios](./advanced.md) →
