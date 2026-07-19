---
title: "Advanced Scenarios"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 30
---

Scenarios 20-27 move from single-decision artifacts to the judgment calls that hold a whole team's
direction together: setting technical strategy, predicting Conway's Law's effect on a reorg,
guardrailing DORA metrics against gaming, calibrating delegation differently for two different
reports, trading delivery speed against growth deliberately, institutionalizing a learning norm,
planning succession, and assembling a full, internally coherent leadership decision set. All
scenarios continue following **Everline**'s Platform team, led by **Priya Kapoor** -- every name,
number, and quote below is an illustrative, constructed example, not a real transcript. Every
artifact below also lives, standalone, under `learning/artifacts/`.

---

### Worked Scenario 20: Technical Strategy Doc

**Context**: Exercises co-12, co-14. Priya writes a one-page technical strategy for the Platform
team's next two quarters, tying each bet to a stated product/business outcome.

**Decision artifact**:

> **Bet 1 -- migrate the ETL pipeline from batch to streaming.** Ties to: reducing the
> dashboard-alerts feature's data latency from ~15 minutes to under 1 minute, which is the specific
> gap product has flagged as blocking a premium-tier alerting offer. **Trade-off**: streaming
> infrastructure is more operationally complex than batch, meaning higher on-call learning curve for
> at least one quarter while the team builds streaming-specific runbooks.
>
> **Bet 2 -- adopt schema-registry contract testing across every producer/consumer boundary.** Ties
> to: cutting cross-team schema-break incidents (2 last month alone, per Worked Scenario 18) toward
> zero, protecting both Platform's and Data Science's on-call load. **Trade-off**: every schema
> change gets a mandatory contract-test gate, adding a small amount of friction to changes that used
> to ship immediately.
>
> **Bet 3 -- reduce on-call noise by tuning alert thresholds and removing alerts with no actionable
> runbook.** Ties to: engineer retention -- pager fatigue was the top cited reason in this quarter's
> team survey for two people considering leaving the on-call rotation entirely. **Trade-off**: a
> small number of real-but-rare issues will surface later (via the next day's dashboard check
> instead of a page) rather than immediately.
>
> **Explicitly not this year**: a full rewrite of the ingestion service in a different language --
> real cost, no stated product outcome justifies it right now.

**Verify**: every named bet traces to a stated product/business outcome (dashboard-alert latency,
schema-break incident reduction, retention) and states its trade-off explicitly (operational
complexity, contract-test friction, delayed visibility on rare issues) -- satisfying co-12 and
co-14's rule.

**Key takeaway**: The strategy also names what it's explicitly _not_ doing this year (the full
rewrite) -- a strategy that only lists bets without naming what it declines is really just a wish
list; naming the rejected option is part of what makes this one a real strategy.

**Why It Matters**: Without this document, the team still makes technical bets constantly -- through
a hundred small unstated defaults in day-to-day work -- except nobody chose them deliberately, and
six months from now nobody could explain why the system looks the way it does or whether it's
working.

---

### Worked Scenario 21: Conway's Law Reorg Memo

**Context**: Exercises co-18. As the Platform team grows past 10 people, Priya proposes splitting
it into two sub-teams and predicts the resulting system-boundary shift.

**Decision artifact**:

> **Proposed split**: an "Ingestion" sub-team (owns event intake, validation, the streaming
> pipeline from Worked Scenario 20's Bet 1) and a "Serving" sub-team (owns the query API and
> dashboard-facing data layer that consumes what Ingestion produces).
>
> **Conway's Law prediction**: per Conway's Law, the two teams' communication structure -- a
> hand-off between two separate teams instead of one team owning the whole pipeline -- will produce
> a correspondingly formal boundary in the system itself. Specifically, I predict the currently
> informal, frequently-changed internal event format between ingestion and the query layer will
> harden into a versioned, contract-tested API within two quarters, because two separate teams
> can no longer coordinate an informal shared-format change with a same-day Slack message the way
> one team could.
>
> **Explicit acceptance of that trade-off**: this is a deliberate cost, not an accident -- a
> versioned contract between the two layers is exactly the schema-registry discipline Worked
> Scenario 20's Bet 2 was already pushing toward, so the reorg accelerates a boundary the team wanted
> anyway.

**Verify**: the memo names Conway's Law explicitly and states the predicted new system boundary (an
informal internal format hardening into a versioned, contract-tested API between the two new
sub-teams) -- satisfying co-18's rule.

**Key takeaway**: The memo doesn't just describe the new org chart -- it predicts, before the split
happens, exactly which part of the system will change shape as a result, which means Priya can check
later whether the prediction held.

**Why It Matters**: A reorg planned purely around headcount and reporting lines, with no attention
to Conway's Law, regularly produces a system boundary nobody wanted or predicted -- naming the
predicted boundary in advance turns a surprise six months later into a deliberate, accepted design
choice made up front.

---

### Worked Scenario 22: DORA-Goodhart Guardrail

**Context**: Exercises co-11. After Worked Scenario 11's diagnostic memo, a few engineers start
half-jokingly asking if deployment frequency is now "a number we're supposed to hit." Priya designs
a guardrail before that becomes real behavior.

**Decision artifact**:

> **The gaming risk being guarded against**: deployment frequency, treated as an individual or
> team target rather than a diagnostic, can be inflated by splitting one meaningful change into
> several trivial deploys (a whitespace commit, then the real change, then a comment fix) -- the
> number goes up, the underlying delivery capability doesn't.
>
> **The guardrail**: DORA numbers stay reported at the team level only, reviewed quarterly as a
> diagnostic input to the next prioritization pass (as in Worked Scenario 10 and 20), never
> reported per-engineer and never referenced in any individual's performance calibration (Worked
> Scenario 13). Alongside deployment frequency, the team also tracks a simple qualitative check each
> quarter: "did anything ship this quarter that felt trivially split just to move the number?" --
> asked directly in the retro, so gaming would have to survive being named out loud by a teammate.

**Verify**: the design names the specific gaming path (splitting one change into several trivial
deploys to inflate the count) and a concrete countermeasure (team-level-only reporting, explicit
exclusion from individual calibration, plus a direct retro question) -- satisfying co-11's rule.

**Key takeaway**: The fix isn't "trust people not to game it" -- it's structural: the metric is
deliberately kept out of any context (individual performance) where gaming it would pay off, and a
recurring direct question makes gaming socially visible if it happens anyway.

**Why It Matters**: The moment a metric becomes a target tied to an individual's evaluation, someone
will find a way to move the number without moving the underlying outcome -- Goodhart's dynamic
applies to DORA exactly as much as any other metric, and the guardrail has to be designed before
gaming starts, not after.

---

### Worked Scenario 23: Autonomy-vs-Alignment Calibration

**Context**: Exercises co-08, co-04. Jordan (senior, high track record) and Alex (still building
judgment, per Worked Scenario 4) both need a delegation approach, but not the same one. Priya
calibrates each and justifies why.

**Decision artifact**:

> **Jordan -- high autonomy**: readiness signal -- three consecutive quarters of design proposals
> that survived review with only minor changes (Worked Scenario 13's calibration criteria), plus the
> caching decision from Worked Scenario 7, made independently and correctly. Delegation approach:
> Jordan gets the what-and-why brief and picks the how with no required check-in; Priya reviews
> outcomes after the fact, not the approach in advance.
>
> **Alex -- more direction, for now**: readiness signal -- Worked Scenario 4's validation-placement
> question needed three coaching questions to resolve, and this is still Alex's first two-way
> architectural trade-off without a senior engineer pairing directly. Delegation approach: Alex gets
> the same what-and-why brief, plus a required design-review checkpoint before implementation starts
> -- not because Alex isn't capable, but because the evidence of independent judgment on this class
> of decision isn't there yet.

**Verify**: each calibration cites a specific readiness signal (Jordan's three-quarter track record
of independently correct proposals; Alex's still-forming judgment on this specific decision class),
not a uniform policy applied identically to both -- satisfying co-08 and co-04's rule.

**Key takeaway**: The difference isn't about who's more "trusted" as a person -- it's about
demonstrated evidence on this specific class of decision. Alex's required checkpoint isn't a
punishment; it's calibrated to where the evidence currently is, and it will change as more evidence
accumulates.

**Why It Matters**: Applying the same delegation level to every report -- either universal high
autonomy or universal tight oversight -- either sets someone like Alex up to make an expensive
mistake alone, or insults someone like Jordan by second-guessing decisions that have already earned
independence.

---

### Worked Scenario 24: Delivery-vs-Growth Trade-off Memo

**Context**: Exercises co-01, co-05. A high-visibility stretch assignment (leading the streaming
migration from Worked Scenario 20's Bet 1) needs an owner under real deadline pressure. Jordan would
finish it fastest; Maya would grow the most from leading it, per her growth plan (Worked Scenario 5).
Priya decides and states the trade-off.

**Decision artifact**:

> **The decision**: Maya leads the streaming migration, with Jordan available as a design-review
> resource, not the implementer.
>
> **What's being traded**: near-term speed for future team capability. Jordan would very likely
> deliver this specific migration faster and with fewer false starts -- Jordan has done something
> structurally similar before. Giving it to Maya means a slower path to done and a real chance of
> needing a course-correction Jordan wouldn't have needed. What it buys: this is exactly the
> "proposes a design approach and defends a trade-off" next-level behavior Maya's growth plan names
> (Worked Scenario 5) -- leading a real migration under real stakes is a categorically different
> practice opportunity than a design note reviewed in a 1:1.
>
> **The mitigation for the deadline risk**: Jordan reviews Maya's design before implementation
> starts (the same checkpoint pattern as Worked Scenario 23's Alex calibration), so the deadline
> risk from a possible course-correction is caught early, not discovered at the end.

**Verify**: the memo explicitly states what is traded -- near-term speed (Jordan would be faster)
versus future team capability (Maya's growth) -- rather than presenting the choice as costless,
satisfying co-01 and co-05's rule.

**Key takeaway**: Priya doesn't pretend Maya is equally fast -- she names the real cost of the
choice and pairs it with a specific mitigation (Jordan's design review) that manages the deadline
risk without erasing the growth opportunity by quietly reassigning it to Jordan under pressure.

**Why It Matters**: Under real deadline pressure, the reflexive choice is almost always "give it to
whoever's fastest" -- which optimizes this one deadline while quietly starving the team's future
capacity, because the person who most needed the stretch assignment never gets one when it actually
matters.

---

### Worked Scenario 25: Learning-Norm Institutionalization

**Context**: Exercises co-19. Priya wants the Platform team's ad hoc "someone shares something
interesting sometimes" habit to become a durable norm that survives her own eventual departure.

**Decision artifact**:

> **The ritual**: a 20-minute rotating tech-talk slot in the team's existing biweekly all-hands,
> already on the calendar -- no new meeting created.
>
> **The mechanism that keeps it running without its original owner**: facilitation ownership is
> tied to the same rotation calendar Worked Scenario 19's postmortem-facilitator duty already uses,
> not to Priya personally scheduling speakers each time. Whoever is up on the rotation picks their
> own topic (a recent design decision, a postmortem's root cause, a tool they learned) and the
> calendar entry itself, not a person, is what triggers the next talk. If Priya left tomorrow, the
> calendar keeps generating the next slot and the next name on the rotation regardless.

**Verify**: the design names the specific mechanism (a shared, standing rotation calendar that
generates the next speaker automatically) that keeps the ritual running once its original owner
leaves, not merely a stated intention to "keep doing this" -- satisfying co-19's rule.

**Key takeaway**: Reusing the existing rotation infrastructure (the same calendar already driving
postmortem-facilitator duty) means the learning norm doesn't need its own separate maintenance --
it inherits the same durability the rotation already has.

**Why It Matters**: A learning habit that depends on one enthusiastic person's personal initiative
to schedule and chase speakers evaporates the exact week that person is busy, out sick, or gone for
good -- tying it to a mechanism instead of a person is the only version that survives past any one
manager's tenure, including Priya's own.

---

### Worked Scenario 26: Succession-and-Delegation Plan

**Context**: Exercises co-08, co-01. Priya wants to grow Jordan into a future tech-lead role by
progressively delegating her own responsibilities, not all at once.

**Decision artifact**:

> **Transfer order and trigger signals**:
>
> 1. **First: sprint-planning facilitation.** Trigger to start: Jordan has already run two planning
>    sessions informally when Priya was out (observed evidence, not a guess). Jordan facilitates
>    every planning session going forward; Priya attends as a participant only.
> 2. **Second (once #1 is stable for a full quarter): on-call escalation ownership** -- being the
>    first call when an incident needs a decision beyond the on-call engineer's authority. Trigger
>    to start: Jordan has independently led two production incidents to resolution (Worked Scenario
>    2 is one data point already).
> 3. **Third (once #2 is stable): representing the team in roadmap negotiations with product**
>    (the role Priya played in Worked Scenario 15). Trigger to start: Jordan has written at least one
>    trade-off memo, reviewed and endorsed by Priya, that could have been sent to product as-is.
>
> **What stays with Priya for now**: hiring decisions and performance calibration -- these transfer
> last, once Jordan is functioning as a de facto lead across the first three areas.

**Verify**: the plan names which decisions transfer first (sprint-planning facilitation, then
on-call escalation, then roadmap representation) and the observable signal that triggers each
transfer (informally already doing it; independently resolved incidents; an endorsable trade-off
memo) -- satisfying co-08 and co-01's rule.

**Key takeaway**: Nothing transfers on a calendar date -- each step is gated on observed evidence
that Jordan is already operating at that level, not on Priya's estimate of how long training "should"
take.

**Why It Matters**: Delegating everything at once overwhelms even a strong report and sets them up
to fail publicly; delegating nothing until Priya feels fully ready to let go never actually happens
-- a staged plan with observable triggers is what turns "I should grow a successor eventually" into
something that actually occurs on a real timeline.

---

### Worked Scenario 27: Full Leadership Decision Set

**Context**: Exercises co-01, co-05, co-06, co-10, co-12, co-13, co-14. Ahead of Q4 planning, Priya
assembles three artifacts -- a growth plan, a prioritization decision record, and a technical
strategy note -- into one internally coherent leadership decision set for the Platform team.

**Decision artifact**:

> **Growth plan (Chris, Engineer -> Senior Engineer)**: building on Worked Scenario 13's
> calibration evidence (two adopted design notes this quarter), the next-level behavior to practice
> is leading a design review for someone else's proposal, not just writing his own -- the ladder rung
> for "reviews and improves others' designs, not just proposes his own" is the named gap.
>
> **Prioritization decision record (Q4)**: competing demands are the Conway's-Law-driven reorg
> (Worked Scenario 21), the remaining two-thirds of the ETL rewrite (Worked Scenario 10 covered only
> the highest-risk third), and a customer-escalated request for faster multi-currency support
> (Worked Scenario 15). Decision: execute the reorg first (a structural change is cheaper before more
> work lands on the current team shape), continue the ETL rewrite in parallel at reduced pace, and
> hold the multi-currency acceleration request until Q1 -- communicated to product with the same
> reasoning style as Worked Scenario 15's memo.
>
> **Technical strategy note (Q4 addendum)**: reaffirms Worked Scenario 20's three bets, adding that
> Bet 2 (schema-registry contract testing) is now higher-priority given the reorg's predicted
> boundary hardening (Worked Scenario 21) -- the contract-testing discipline needs to be in place
> before the Ingestion/Serving split, not after, or the boundary will harden around an undocumented
> format instead of a versioned one.
>
> **Coherence check**: Chris's growth assignment (leading design reviews) directly supports the
> contract-testing rollout the strategy note just re-prioritized -- reviewing other engineers'
> contract-test designs is a concrete, real venue for exactly the next-level behavior his growth plan
> names. No artifact contradicts another: the reorg proceeds before the ETL work slows further, and
> the strategy's newly-elevated priority (contract testing) has a named engineer (Chris) growing into
> exactly the skill it needs.

**Verify**: all three artifacts reference the same team context (the Platform team's Q4, building
directly on Worked Scenarios 10, 13, 15, 20, and 21) and no trade-off in one contradicts another --
the coherence check makes the cross-references explicit -- satisfying every cited `co-NN`'s rule
simultaneously.

**Key takeaway**: None of these three artifacts was written from scratch -- each one explicitly
built on evidence and decisions already established earlier in this topic, which is exactly what
makes them checkably coherent instead of three separately plausible documents that happen to sit
next to each other.

**Why It Matters**: A growth plan, a prioritization record, and a technical strategy written in
isolation from each other routinely end up quietly working against one another -- a growth
assignment that has nothing to do with the strategy's actual priorities, or a prioritization
decision that ignores a reorg the strategy already committed to. Checking them against each other
explicitly is what turns three documents into one coherent leadership picture.

---

← Previous: [Intermediate Scenarios](./intermediate.md) · Next: [Capstone](./capstone/overview.md) →
