---
title: "Beginner Scenarios"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 10
---

Scenarios 1-10 establish the single-decision discipline every later scenario in this topic builds
on: naming an outcome instead of a feature, framing a problem before a solution, writing a job
story, running a Mom Test interview, scoring one feature with RICE, bucketing a backlog with
MoSCoW, sorting initiatives on an impact-effort grid, mapping a funnel, and spotting vanity
metrics. Most scenarios follow **Kestrel**, a fictional shift-scheduling SaaS for small retail and
restaurant teams -- every manager quote and interview answer below is an illustrative, constructed
example written to teach the technique, not a real transcript. Every artifact below also lives,
standalone, under `learning/artifacts/`.

---

### Worked Scenario 1: Outcome-vs-Output Rewrite

**Context**: Exercises co-01. Three feature-request tickets have landed in Kestrel's backlog,
each written as a solution with no stated outcome.

**Decision artifact**:

> **Ticket A -- "Add a CSV export button to the schedule page."**
> Rewritten as outcome: managers who currently retype last week's hours into payroll by hand cut
> payroll prep from about 45 minutes to under 5, and stop making the copy-paste transcription
> errors that retyping introduces.
>
> **Ticket B -- "Add dark mode."**
> Rewritten as outcome: night-shift managers who build tomorrow's schedule around 11pm stop
> squinting at a bright white screen and stop abandoning the draft schedule early because the glare
> makes their eyes hurt.
>
> **Ticket C -- "Add a 'duplicate shift' button."**
> Rewritten as outcome: managers who run the same weekly shift pattern build next week's full
> schedule in under 2 minutes, instead of re-entering every individual shift by hand.

**Verify**: each rewrite names a change in what the manager _does_ (prep time drops, they stop
squinting and stop abandoning the draft, scheduling drops to under 2 minutes) rather than a UI
element -- satisfying co-01's rule that removing every feature noun still leaves a testable
behavior claim standing.

**Key takeaway**: None of the three original tickets was deleted or replaced -- the button, the
theme, and the shortcut may all still get built. What changed is that each ticket now states _why_
it's worth building, in terms a reviewer can actually contest or confirm later.

**Why It Matters**: A backlog of solution-only tickets can be fully "delivered" -- every button
shipped, every checkbox ticked -- while the underlying problems (slow payroll prep, eye strain at
11pm, slow schedule building) remain completely unsolved, because nothing in the ticket ever
committed the team to checking whether they actually got solved.

---

### Worked Scenario 2: Problem Statement From a Request

**Context**: Exercises co-02. A restaurant owner emails Kestrel's product team: "Can you make
scheduling easier?"

**Decision artifact**:

> **Problem statement**: Restaurant shift managers who build next week's schedule every Thursday
> afternoon -- juggling a paper availability list and a scattered thread of staff text messages --
> currently spend 40-60 minutes per week on it and still make 1-2 double-booking mistakes a month.
> We want both the time spent and the mistake rate down. This statement does not yet commit to any
> specific redesign of the scheduling flow, an availability-collection feature, or a conflict
> checker -- which of those (if any) is worth building is a separate, later decision.

**Verify**: the statement names the user (restaurant shift managers), the circumstance (every
Thursday afternoon, juggling paper and texts), and the desired outcome (less time, fewer
double-bookings) -- and no specific feature or UI is named anywhere in it, satisfying co-02's rule
that the solution stays withheld.

**Key takeaway**: "Make scheduling easier" and this problem statement describe the same underlying
situation -- the rewrite adds nothing the owner didn't already imply, it just makes the implied
parts explicit enough that a team can design against them.

**Why It Matters**: Had the team instead literally built "an easier scheduling UI" without this
step, they'd have had no way to check afterward whether the actual owner-facing pain -- 40-60
minutes and 1-2 mistakes a month -- had improved at all; the redesign could ship, look nicer, and
still leave both numbers unchanged.

---

### Worked Scenario 3: JTBD Job Story

**Context**: Exercises co-03. Kestrel's team wants to understand why managers keep asking for
"a way to see who's available," phrased as a job story rather than a feature request.

**Decision artifact**:

> When one of my best cashiers texts me an hour before their shift saying they're sick, I want to
> instantly see who's already qualified and available to cover, so I can fill the shift without
> calling six people one by one, and still open the store on time.

**Verify**: the job story names the circumstance ("when one of my best cashiers texts me an hour
before their shift"), the motivation ("I want to instantly see who's already qualified and
available"), and the expected progress ("so I can fill the shift... and still open the store on
time") -- all three elements present, satisfying co-03's rule.

**Key takeaway**: The job story never mentions a UI, a screen, or a button -- "instantly see who's
qualified and available" could be solved by a smart filtered list, a one-tap broadcast to eligible
staff, or something else entirely; the job, not a pre-chosen interface, is what's being hired for.

**Why It Matters**: A feature request phrased only as "add an availability filter" would have
missed the actual urgency driving it -- this is a same-day, time-pressured job (fill the shift
_before_ opening), not a leisurely planning task, and that urgency should shape which solution
gets prioritized and how fast it needs to respond.

---

### Worked Scenario 4: Mom Test Interview Script

**Context**: Exercises co-04. Before building anything, Kestrel's product manager wants to
validate interest in an "AI auto-schedule suggestions" idea and drafts six interview questions.

**Decision artifact**:

> 1. Walk me through the last time you built next week's schedule -- what did you actually do,
>    step by step?
> 2. How long did that take you, start to finish, the last time you did it?
> 3. What's the last mistake you made in a published schedule, and how did you find out about it?
> 4. Tell me about the last time you asked someone else to help you build or check a schedule --
>    who, and why?
> 5. What tools or notes did you have open on your screen the last time you scheduled?
> 6. Tell me about the last time you changed a schedule after publishing it -- what happened, and
>    why?

**Verify**: every question asks about a specific past event ("the last time," "what did you
actually do") rather than an opinion or a hypothetical, and none of the six mentions "AI,"
"auto-schedule," or any other pitch of the idea under test -- satisfying co-04's rule.

**Key takeaway**: Not one question asks "would you use AI scheduling?" -- the script is designed
to surface the manager's actual current process and its actual pain points, which is the raw
material a team needs to judge whether an AI-suggestion feature would land anywhere real.

**Why It Matters**: Asking directly about the AI idea would have produced a polite, low-cost "yeah,
sounds neat" from almost anyone -- that answer predicts nothing about real adoption, while a
detailed account of a 55-minute Thursday scheduling ritual with three specific pain points gives
the team something they can actually design against.

---

### Worked Scenario 5: Mom Test Red-Flag Audit

**Context**: Exercises co-04. A junior PM drafts eight interview questions for the same AI
auto-schedule idea; a teammate audits them against the Mom Test before the interviews are booked.

**Decision artifact**:

> 1. "Would you use an AI-suggested schedule if we built one?" -- **flagged**: hypothetical/future
>    prediction.
> 2. "How many hours did you spend on last week's schedule?" -- clean: specific past behavior.
> 3. "Do you think auto-scheduling is a good idea?" -- **flagged**: asks for an opinion.
> 4. "What's the last thing that went wrong with a schedule you published?" -- clean: specific past
>    behavior.
> 5. "Would you pay $20/month extra for this?" -- **flagged**: hypothetical/future prediction.
> 6. "Who else was involved the last time you built a schedule?" -- clean: specific past behavior.
> 7. "Do you think your team would like getting shift reminders by text?" -- **flagged**: opinion
>    about a hypothetical future reaction.
> 8. "Tell me about the last time a shift went uncovered -- what happened right before that?" --
>    clean: specific past behavior.

**Verify**: every flagged question (1, 3, 5, 7) asks for an opinion, a hypothetical, or a future
prediction, and every unflagged question (2, 4, 6, 8) asks about a specific past event --
satisfying co-04's rule exactly for all eight items.

**Key takeaway**: The four flagged questions aren't _bad_ questions in every context -- they're
just the wrong tool for validating whether a real need exists, because every one of them can be
answered politely without costing the respondent anything.

**Why It Matters**: Running the original eight-question script unaudited would have produced four
answers that feel like validation ("yeah, I'd probably use that," "sure, $20 seems fine") but carry
none of the predictive weight of an account of actual past behavior -- the audit catches this
before the interviews, not after the feature ships and adoption disappoints.

---

### Worked Scenario 6: RICE Score for a Single Feature

**Context**: Exercises co-07. Kestrel's team scores the "CSV export" ticket from Worked Scenario 1
using RICE before deciding whether it belongs in the next release.

**Decision artifact**:

| Factor         | Value | Unit                                                                           |
| -------------- | ----- | ------------------------------------------------------------------------------ |
| Reach (R)      | 400   | managers who would use the export, per quarter                                 |
| Impact (I)     | 1     | Intercom's discrete scale (3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal) |
| Confidence (C) | 0.8   | 80%, based on the payroll-prep pain named directly in interviews               |
| Effort (E)     | 2     | person-months                                                                  |

> RICE = (400 × 1 × 0.8) ÷ 2 = 320 ÷ 2 = **160**

**Verify**: the arithmetic equals `(Reach × Impact × Confidence) ÷ Effort` exactly -- (400 × 1 ×
0.8) ÷ 2 = 160 -- and every factor's unit is stated alongside its number, satisfying co-07's rule.

**Key takeaway**: A RICE score is only as trustworthy as its stated units -- "400" alone means
nothing; "400 managers per quarter" is a claim someone can actually check against real usage data
later.

**Why It Matters**: A score of 160, on its own, means nothing outside the context of the rest of
the backlog -- its real value is comparability: once every other candidate feature is scored the
same way, 160 tells the team exactly where CSV export ranks against them, which Worked Scenario 11
does next.

---

### Worked Scenario 7: MoSCoW Bucketing

**Context**: Exercises co-08. Kestrel's team buckets a ten-item backlog into Must / Should /
Could / Won't for the upcoming Q3 release, ahead of a contract closing that quarter that requires
SSO.

**Decision artifact**:

> **Must (this release)**: (1) fix the double-booking scheduling bug; (2) SSO login, required by
> the enterprise contract closing this quarter.
>
> **Should (this release)**: (3) CSV export of schedules; (4) mobile push notifications for shift
> changes.
>
> **Could (this release, if time allows)**: (5) dark mode; (6) a one-way team-messaging
> announcement channel.
>
> **Won't (this release -- not rejected, revisit at the next quarterly planning cycle)**: (7) the
> full AI auto-schedule-suggestion engine; (8) full white-label theming; (9) custom on-prem
> deployment; (10) cross-location shift swaps.

**Verify**: every "Won't" item (7-10) is explicitly labeled "not this release -- revisit at the
next quarterly planning cycle," not stated or implied as a permanent rejection -- satisfying
co-08's rule.

**Key takeaway**: Nothing in the "Won't" bucket is dead -- it's simply not competing for this
quarter's limited capacity, which is a scoping decision, not a verdict on the idea's merit.

**Why It Matters**: Without the explicit "revisit next cycle" framing, engineers who worked hard
shaping the AI auto-schedule idea (item 7) could reasonably read "Won't" as "the team rejected my
work" and disengage from product discovery entirely -- the framing difference between "not now"
and "no" materially affects whether people keep bringing good ideas forward.

---

### Worked Scenario 8: Impact-Effort Quadrant

**Context**: Exercises co-09. Before spending real RICE-scoring effort, Kestrel's team does a
five-minute impact-effort pass across eight candidate initiatives to find the quick wins.

**Decision artifact**:

| Quadrant                                 | Initiatives                                                   |
| ---------------------------------------- | ------------------------------------------------------------- |
| **Quick wins** (high impact, low effort) | CSV export; dark mode                                         |
| Big bets (high impact, high effort)      | AI auto-schedule suggestions; SSO for the enterprise contract |
| Fill-ins (low impact, low effort)        | Confetti animation on publish; adjustable font size           |
| Time sinks (low impact, high effort)     | Full white-label theming; custom on-prem deployment           |

**Verify**: the two initiatives named as quick wins -- CSV export and dark mode -- sit specifically
in the high-impact, low-effort row of the table above, satisfying co-09's rule.

**Key takeaway**: The chart doesn't replace RICE (Worked Scenario 6, 11) -- it's a five-minute
triage across all eight items so the team spends real scoring effort only on the ones that survive
this first cut, rather than RICE-scoring every idea that comes up.

**Why It Matters**: Full white-label theming and custom on-prem deployment both land in "time
sinks" -- high effort, low impact for Kestrel's actual customer base of small retail and restaurant
teams -- and the chart makes that visible in seconds, before either idea consumes a planning
meeting's worth of debate.

---

### Worked Scenario 9: AARRR Funnel Map

**Context**: Exercises co-18. Kestrel's team maps its own signup-to-paid lifecycle onto the five
AARRR stages to see where the funnel actually is, before optimizing anything.

**Decision artifact**:

| Stage       | Concrete event                                                                                                |
| ----------- | ------------------------------------------------------------------------------------------------------------- |
| Acquisition | A manager clicks a Google search ad for "restaurant shift scheduling app" and lands on Kestrel's signup page. |
| Activation  | Within 3 days of signup, the manager publishes their first complete weekly schedule.                          |
| Retention   | In week 2, the same manager logs back in and publishes a second week's schedule.                              |
| Referral    | The manager invites a second location's manager (a different store the same company runs) to join Kestrel.    |
| Revenue     | The team's 14-day free trial converts to a paid monthly plan.                                                 |

**Verify**: each of the five stages names at least one concrete, observable event, and the events
appear in the correct lifecycle order (an ad click before a first schedule, a first schedule
before a second, a second before an invite or a paid conversion) -- satisfying co-18's rule.

**Key takeaway**: Every event in the table is something Kestrel's own product analytics can already
log (a page view, a "schedule published" action, a login timestamp, an invite sent, a plan
upgrade) -- the funnel map only has value once every stage is tied to something the team can
actually measure, not just describe.

**Why It Matters**: "Growth is slow" says nothing about what to fix; this map lets the team ask a
sharper question -- for example, if the acquisition-to-activation ratio is healthy but
week-2-retention is low, the fix belongs somewhere in the product's ongoing value, not in the
signup funnel at all.

---

### Worked Scenario 10: Vanity Metric Audit

**Context**: Exercises co-21. Kestrel's weekly metrics email lists six numbers; the team audits
which are vanity before deciding which ones actually belong on the dashboard that drives
decisions.

**Decision artifact**:

> 1. Total signups (all time) -- **flagged, vanity**: only ever goes up, and no stated decision
>    changes based on its value.
> 2. Weekly active managers who publish a schedule -- actionable: a drop here would trigger a
>    retention investigation.
> 3. Total shifts ever created (all time) -- **flagged, vanity**: cumulative and always rising; no
>    decision is tied to it.
> 4. % of trials that publish a first schedule within 3 days -- actionable: this is the activation
>    metric (Worked Scenario 25); a drop would trigger an onboarding-flow review.
> 5. App Store downloads -- **flagged, vanity**: measures interest, not product value delivered; no
>    decision is tied to it.
> 6. Week-4 retention rate of paid teams -- actionable: a drop below a stated threshold would
>    trigger a churn-intervention outreach.

**Verify**: each flagged metric (1, 3, 5) lacks any stated cause-and-effect tie to a decision --
nothing the team would actually do differently if the number moved -- while each unflagged metric
(2, 4, 6) names the specific decision a change in it would trigger, satisfying co-21's rule.

**Key takeaway**: The flagged metrics aren't being deleted from the product's internal reporting --
they're being removed from the _decision-driving_ dashboard, because a number a team never acts on
doesn't belong competing for attention with the numbers that do drive action.

**Why It Matters**: A weekly email that leads with "12,000 total signups!" creates a false sense of
health even while week-4 retention quietly slides -- vanity metrics are dangerous specifically
because they're easy to feel good about, which crowds out attention from the actionable metrics
that would actually reveal a problem.

---

← Previous: [Overview](./overview.md) · Next: [Intermediate Scenarios](./intermediate.md) →
