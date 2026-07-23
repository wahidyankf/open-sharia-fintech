---
title: "Advanced Scenarios"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 30
---

Scenarios 23-30 move from single-decision artifacts to the judgment calls that hold a whole
product strategy together: choosing a durable north-star, defining activation precisely,
catching a metric being gamed, calling "commit now" inside a discovery cadence, writing a PR-FAQ
before a build, fixing a delivery appetite, and finally assembling several of this topic's
mechanisms into one internally consistent brief. All eight continue the **Kestrel** narrative --
every number and quote below is an illustrative, constructed example written to teach the
technique, not real usage data or a real transcript. Every artifact below also lives, standalone,
under `learning/artifacts/`.

---

### Worked Scenario 23: North-Star and Input Metrics

**Context**: Exercises co-17, co-20. Kestrel's leadership picks a north-star metric and its input
metrics, and explains why it differs from a stage-specific OMTM.

**Decision artifact**:

> **North-star metric**: number of teams with a published schedule active in the last 7 days.
> This measures delivered value directly -- a team only shows up in this number if they're
> actually running their real-world scheduling through Kestrel, not merely signed up for it.
>
> **Input metrics** (levers the team directly controls):
>
> 1. Activation rate -- % of new signups that publish a first complete schedule within 3 days
>    (Worked Scenario 25).
> 2. Weekly schedule-publish rate per active team -- does an activated team keep coming back
>    week over week?
> 3. Shift-swap completion rate -- % of initiated swap requests that reach a final approve/deny,
>    rather than stalling unresolved (feeding Worked Scenario 27's discovery work).
>
> **Why this differs from an OMTM**: the north-star is durable -- it doesn't rotate as the team's
> current focus changes, and it stays the company's single measure of delivered value for as long
> as Kestrel exists in its current form. An OMTM (Croll & Yoskovitz) is deliberately
> stage-specific and temporary -- this quarter's OMTM, while the team is focused on the onboarding
> redesign (Worked Scenario 20), is specifically the 3-day activation rate; next quarter, once
> activation is healthy, the OMTM will rotate to a different input metric while the north-star
> itself stays the same.

**Verify**: the chosen north-star measures delivered value (active real-world usage, not a vanity
signup count) and each of the three input metrics is a lever the team directly controls, and the
writeup explicitly distinguishes the durable north-star from the stage-specific, rotating OMTM --
satisfying co-17's and co-20's combined rule.

**Key takeaway**: The north-star and the current OMTM can be, and often are, different metrics at
the same time -- the north-star is the scoreboard; the OMTM is whichever lever the team is
currently pulling hardest to move that scoreboard.

**Why It Matters**: A team that conflates the two ends up rotating its "true" success metric every
quarter along with its current project focus -- losing the ability to answer a simple question
("is the product, overall, delivering more value than a year ago?") because the yardstick itself
kept changing.

---

### Worked Scenario 24: HEART Goals-Signals-Metrics

**Context**: Exercises co-19. Kestrel's team fills in a HEART row for one product goal -- Task
Success -- for the core "build and publish a schedule" flow.

**Decision artifact**:

| Element | Content                                                                                                                                                                                   |
| ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Goal    | Managers can publish a correct, conflict-free weekly schedule quickly.                                                                                                                    |
| Signal  | A manager completes a schedule-publish attempt without hitting a validation error (a detected double-booking or an under-staffed shift) and without abandoning the draft partway through. |
| Metric  | % of schedule-publish attempts that succeed on the first try; median time from opening a draft to publishing it.                                                                          |

**Verify**: goal, signal, and metric are all present, and each is mutually consistent with the
others -- the metric plausibly measures the signal (first-try success and time-to-publish both
reflect "completed without hitting an error or giving up"), and the signal plausibly indicates
progress toward the stated goal -- satisfying co-19's rule.

**Key takeaway**: The metric isn't "time to publish" chosen because it's easy to log -- it's
chosen because the Goal -> Signal -> Metric chain traces back to it: a manager hitting a
validation error or abandoning a draft is the concrete, observable signal that the underlying
task-success goal isn't being met, and the metric quantifies exactly that signal.

**Why It Matters**: Picking a metric without first walking the Goals -> Signals -> Metrics chain
invites Goodharting later (co-22) -- if "time to publish" had been chosen with no stated goal
behind it, a team could quietly game it (auto-publish a barely-checked draft) without anyone
noticing the underlying task-success goal was being undermined, because nothing tied the metric
back to what it was supposed to represent.

---

### Worked Scenario 25: Activation Metric Definition

**Context**: Exercises co-20. Kestrel's team defines "activation" precisely, since "logged in
once" was the previous, too-vague definition.

**Decision artifact**:

> **Activation event**: a new team's manager publishes their first complete weekly schedule --
> every open shift for the coming week assigned to a specific staff member -- within 3 days of
> signing up.
>
> **Why this and not "created an account" or "added one employee"**: creating an account or adding
> a single employee record costs the manager almost nothing and delivers no value on its own --
> neither event corresponds to Kestrel actually replacing the manager's prior paper-and-texts
> process (Worked Scenario 2's problem statement) for even a single week.
>
> **Measurement**: the signup timestamp and the first-schedule-published timestamp for every
> team, published to the analytics pipeline as `days_to_first_publish`; a team "activates" if that
> value is ≤ 3 days.

**Verify**: the definition names the first genuine value moment (a complete first schedule
published, not merely an account or a single employee record) and states exactly how it's
measured (the timestamp delta, with a stated 3-day threshold) -- satisfying co-20's rule.

**Key takeaway**: This activation definition is deliberately strict -- "complete" schedule, not
"partial" -- because a manager who publishes a half-finished schedule and abandons it hasn't
actually replaced their old process yet, even though a looser definition might have counted them
as activated.

**Why It Matters**: This precise, falsifiable definition is exactly what makes activation rate a
usable input metric for the north-star (Worked Scenario 23) and the experiment's primary metric
(Worked Scenario 20) -- a vague definition like "logged in once" would inflate the number without
telling the team anything real about whether new teams are getting value.

---

### Worked Scenario 26: Goodhart Guardrail Memo

**Context**: Exercises co-22. Kestrel's support team was measured on "shifts created per week"
(intended as a proxy for customer engagement); the metric rose steadily for a month while the real
activation number (Worked Scenario 25) stayed flat. A PM investigates and writes the memo.

**Decision artifact**:

> **What happened**: support agents, evaluated in part on "shifts created per week" across the
> accounts they onboard, started proactively creating draft placeholder shifts on new customers'
> behalf during onboarding calls -- framed internally as "helping them get started." The metric
> climbed. The actual activation signal (a manager publishing their own complete first schedule,
> Worked Scenario 25) did not move at all during the same period.
>
> **Gaming path named**: "shifts created" counted _any_ shift row inserted into the system,
> regardless of who created it or whether it was ever published -- support staff optimizing for
> their own eval metric found a legitimate-looking action (helping a customer) that inflated the
> number without producing the underlying outcome (a customer actually running their own
> scheduling) the metric was meant to represent.
>
> **Countermeasure**: redefine the support team's metric to count only shifts that are (a)
> published, not drafts, and (b) created by the customer's own user account, not a support agent's
> internal tooling account. Pair this redefined metric with the existing activation-rate guardrail
> (Worked Scenario 25) -- if "customer-published shifts" ever rises without activation rate also
> rising, that is itself now a signal worth re-investigating.

**Verify**: the memo names the specific gaming path (support-created placeholder shifts inflating
a metric that didn't distinguish creator or draft status) and a concrete countermeasure (redefine
the metric to customer-published-only, paired with the activation-rate guardrail) -- satisfying
co-22's rule.

**Key takeaway**: The support agents weren't acting maliciously -- "help the customer get started"
is a reasonable-sounding action that happened to also move their own eval number, which is exactly
Goodhart's Law in its most common, non-adversarial form: people rationally optimize whatever
they're actually measured on.

**Why It Matters**: Had the flat activation number gone uninvestigated because "shifts created"
looked healthy, Kestrel's leadership could have kept believing onboarding was improving for weeks
while the metric that actually mattered (real managers getting real value) stayed exactly where it
started.

---

### Worked Scenario 27: Discovery-vs-Delivery Balance

**Context**: Exercises co-24, co-06. Kestrel's team has spent five weeks interviewing managers
about a shift-swap-approval redesign (the opportunity named in Worked Scenario 19) without
shipping anything, and a new round of interviews is already booked.

**Decision artifact**:

> **Riskiest assumption at stake**: will managers actually trust a faster, one-tap approval flow
> enough to stop manually reviewing every swap request line by line?
>
> **Evidence so far**: interviews 1 through 8 surfaced new detail each time. Interviews 9 through
> 12 repeated the same core finding without adding anything new: managers _want_ faster approval
> specifically for routine, same-role, same-shift-length swaps, but still want to manually review
> anything unusual (a swap across roles, or into overtime). That is a saturation point -- the
> riskiest assumption is already validated with enough confidence to build against.
>
> **Commit-now call**: stop scheduling further discovery interviews on this specific question.
> Commit to building a scoped prototype now -- fast-path approval for routine swaps, manual review
> preserved for anything unusual -- and let real usage (not further interviews) surface whatever
> the interviews couldn't.

**Verify**: the writeup names the riskiest-assumption-validated stop rule -- interview saturation
(new interviews stopped producing new information) combined with the specific riskiest assumption
already being resolved with enough confidence -- as the reason to commit now, satisfying the
combined co-24/co-06 rule.

**Key takeaway**: "Enough discovery" isn't a fixed number of interviews -- it's the point where
additional interviews stop changing what the team would build, which is exactly what interviews 9
through 12 demonstrated here.

**Why It Matters**: A team with no stop rule can keep discovering indefinitely, because there's
always one more manager who might say something new -- naming saturation explicitly is what turns
"we've done enough research" from a vague feeling into a defensible, evidence-based call to start
building.

---

### Worked Scenario 28: PR-FAQ, Working Backwards

**Context**: Exercises co-23. Before building the fast-path swap-approval flow (Worked Scenario
27), Kestrel's team writes a one-page PR-FAQ.

**Decision artifact**:

> **Press release**
>
> _Kestrel launches one-tap shift-swap approval._ Managers currently review every shift-swap
> request the same way, whether it's a routine same-role swap between two trusted staff or an
> unusual cross-role request into overtime -- and swap requests often sit unapproved for hours
> because the review, buried in email or in-app notifications, gets missed. Starting today,
> Kestrel automatically fast-tracks routine, same-role, same-shift-length swaps to a single SMS
> reply ("Y" to approve), while anything unusual still routes to the manager's full review queue.
> "I used to lose track of swap requests in my inbox for half a day," said one early-access
> manager. "Now the easy ones just get handled."
>
> **FAQ**
>
> - _What counts as "routine"?_ Same role, same shift length, both employees already qualified for
>   the shift, requested more than 4 hours before the shift starts.
> - _What if a manager replies with an ambiguous SMS (not a clear "Y")?_ The request stays pending
>   and routes to the full in-app review queue rather than guessing at intent.
> - _What if two managers both have approval rights and both reply?_ The first valid reply wins;
>   the second reply receives an SMS noting the request was already resolved.
> - _Does this remove manager oversight entirely?_ No -- managers can disable fast-path approval
>   for their team at any time, reverting every swap to full manual review.

**Verify**: the press release states the customer's problem (slow, easily-missed swap review for
requests that don't actually need close scrutiny) before naming the solution, and the FAQ answers
the top risks (ambiguous replies, dual-approver races, loss of oversight) rather than only easy
questions -- satisfying co-23's rule.

**Key takeaway**: Writing the press release first forced a precise definition of "routine" before
a single line of the approval logic was built -- that definition became the FAQ's first answer and,
later, the actual fast-path eligibility rule in the shipped feature.

**Why It Matters**: The "does this remove manager oversight entirely" question is exactly the kind
of objection a manager would raise in a sales call or a support ticket after launch -- answering it
here, before the build, is far cheaper than discovering during a live incident that no opt-out
existed.

---

### Worked Scenario 29: Shape Up Pitch

**Context**: Exercises co-25. Kestrel's team pitches the fast-path swap-approval feature (Worked
Scenario 28) at a betting table using Shape Up's fixed-appetite format.

**Decision artifact**:

> **Appetite**: 6 weeks, fixed. Not an estimate -- if the shaped solution below can't be built to a
> demoable state in 6 weeks, the scope shrinks; the appetite does not extend.
>
> **Problem**: routine shift-swap requests sit unapproved for hours because manual review, buried
> in notifications, gets missed (Worked Scenario 27).
>
> **Solution outline** (breadboard level): an approval queue screen for unusual swaps; a fast-path
> SMS one-tap reply for routine swaps meeting the FAQ's eligibility rule; a per-team toggle to
> disable fast-path entirely.
>
> **Rabbit holes** (explicitly named, to avoid): do not build a general-purpose, configurable
> approval-workflow engine -- the eligibility rule is fixed logic, not a rules builder. Do not
> support swap chains involving more than two people (A swaps with B who swaps with C) -- single
> pairwise swaps only, this cycle.
>
> **No-gos**: cross-location shift swaps (a shift moving between two different store locations) --
> explicitly out of scope for this cycle, revisit later.
>
> **Circuit-breaker**: if the fast-path SMS flow and the per-team toggle aren't both demoable by
> the end of week 5, cut the approval-queue screen redesign from this cycle's scope and ship
> fast-path-only against the existing review screen, rather than extending the appetite past 6
> weeks.

**Verify**: the appetite is stated as a fixed 6-week time budget (not an estimate derived from the
scope), and a circuit-breaker is explicitly named -- what happens, and when, if the work isn't
demoable on schedule -- satisfying co-25's rule.

**Key takeaway**: The rabbit holes and no-gos aren't afterthoughts -- naming them up front is what
keeps the fixed 6-week appetite realistic; without them, "shift-swap approval" could quietly grow
to include a workflow engine and cross-location support, neither of which fits the stated budget.

**Why It Matters**: Without a circuit-breaker, a team under schedule pressure in week 6 faces an
unstated choice between shipping something broken or silently asking for more time -- naming the
fallback (fast-path-only, existing review screen) in advance turns that pressure-moment decision
into one the team already agreed to before the cycle even started.

---

### Worked Scenario 30: Full Product Brief Consistency

**Context**: Exercises co-01, co-07, co-12, co-15, co-17. Kestrel's team assembles the fast-path
swap-approval work (Worked Scenarios 27-29) into one compact brief and checks it for internal
consistency before the betting table finalizes it.

**Decision artifact**:

> **Problem/outcome (co-01)**: managers currently lose track of routine swap requests for hours;
> the outcome sought is routine swaps resolved within minutes, not a new "approval screen" feature
> for its own sake.
>
> **MVP scope (co-12)**: fast-path SMS approval for routine, same-role, same-shift-length swaps
> only (the riskiest-assumption test from Worked Scenario 27), with a per-team disable toggle;
> explicitly not a general workflow engine and not cross-location swaps (Worked Scenario 29's
> rabbit holes and no-gos).
>
> **RICE-ranked mini-backlog (co-07)**:
>
> | Item                           | Reach (per quarter) | Impact | Confidence | Effort (person-months) | RICE                        |
> | ------------------------------ | ------------------- | ------ | ---------- | ---------------------- | --------------------------- |
> | Fast-path SMS approval         | 500                 | 2      | 0.8        | 3                      | (500×2×0.8)÷3 = **266.7**   |
> | Per-team disable toggle        | 500                 | 0.5    | 1.0        | 0.5                    | (500×0.5×1.0)÷0.5 = **500** |
> | Approval-queue screen redesign | 300                 | 1      | 0.5        | 2                      | (300×1×0.5)÷2 = **75**      |
>
> Ranked: disable toggle (500) > fast-path approval (266.7) > queue redesign (75) -- consistent
> with Worked Scenario 29's circuit-breaker, which keeps the toggle and the fast-path flow and cuts
> the queue redesign first if time runs short.
>
> **Metrics (co-17)**: this feature is one of the north-star's three input-metric levers (shift-
> swap completion rate, Worked Scenario 23) -- success here should move that input metric directly.
>
> **Experiment (co-15)**: hypothesis -- fast-path approval reduces median swap-request-to-decision
> time without increasing manager-reported wrong-approvals. Primary metric (OEC): median time from
> swap request to a final decision. Guardrail: manager-reported incorrect approvals (a swap that
> shouldn't have qualified as "routine" but was auto-approved) must not increase.

**Verify**: the brief's scope serves the stated problem (fast-path approval, not a broader
workflow engine, directly targets "routine swaps lose hours"), the metrics measure the stated
outcome (swap completion rate is a named north-star input, not an unrelated vanity number), and
the experiment tests the stated hypothesis (median decision time, guarded against a specific named
harm) -- satisfying co-01/co-07/co-12/co-15/co-17's combined consistency rule.

**Key takeaway**: Every section of this brief was already built, individually, across Worked
Scenarios 27-29 -- assembling them side by side is what surfaces whether they actually agree with
each other, which the RICE ranking's alignment with the circuit-breaker's cut order confirms here.

**Why It Matters**: A brief where the MVP scope, the backlog ranking, and the pitch's circuit-
breaker silently disagreed (for example, if RICE had ranked the queue redesign highest while the
circuit-breaker planned to cut it first) would send the engineering team mixed signals about what
actually matters if time runs short -- checking consistency explicitly is what this topic's own
capstone does next, at a larger scale, for a different Kestrel feature.

---

← Previous: [Intermediate Scenarios](./intermediate.md) · Next: [Capstone](./capstone/overview.md) →
