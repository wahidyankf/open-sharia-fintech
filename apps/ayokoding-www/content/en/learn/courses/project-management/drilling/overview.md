---
title: "Overview"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Project Management topic: recall first, then
applied judgment, then hands-on artifact repair, then a checklist to confirm real automaticity, and
finally why/why-not prompts that test whether you can explain the reasoning, not just produce the
artifact. Every answer is hidden in a `<details>` block; try each item yourself before opening it.

This topic has no runnable interpreter -- every "kata" below is a decision-artifact repair drill
instead of a code fix, verified the same observable-property way this topic's worked scenarios were
verified (a named field present, a computed score matching a rule), not by running anything.

## Recall Q&A

Fifteen short-answer questions, one per concept (`co-01` through `co-15`). Answer from memory, then
check.

**Q1 (co-01 -- triple-constraint).** Scope, schedule, and cost form a triangle. What is the
professional move when reality departs from the original estimate, and what happens if nobody makes
that move explicitly?

<details>
<summary>Answer</summary>

Decide, at the start, which two constraints are genuinely fixed and let the third become the
dependent variable everyone tracks explicitly. If nobody makes this move, the trade-off still
happens -- just silently, usually as a quality cut nobody notices until it is too late to reverse
cheaply.

</details>

**Q2 (co-02 -- delivery-methodologies).** Name the context property that should drive a choice
between waterfall, Scrum, and Kanban for a given team.

<details>
<summary>Answer</summary>

The shape of the work: waterfall fits a high cost of course-correction with stable, externally
mandated requirements; Scrum fits a high rate of requirement change with an engaged customer who can
reprioritize every sprint; Kanban fits continuous, unpredictable work arrival with no natural
iteration boundary. The methodology should follow the work's shape, not fashion.

</details>

**Q3 (co-03 -- work-breakdown-structure).** What two-part test must every WBS leaf pass?

<details>
<summary>Answer</summary>

Independently estimable (a team member could size it without decomposing it further) and
independently assignable (one name or one pair can own it end to end without splitting it across
unrelated owners).

</details>

**Q4 (co-04 -- dependency-graph-and-critical-path).** What is the critical path, and what is true of
every task on it?

<details>
<summary>Answer</summary>

The single longest cumulative-duration chain from start to finish in the dependency graph. Every
task on it has zero slack: delaying it by one day delays the whole project by one day.

</details>

**Q5 (co-05 -- estimation-points-velocity).** Why do story points estimate size relative to a
reference story instead of duration in hours, and how does velocity turn that into a forecast?

<details>
<summary>Answer</summary>

Relative sizing embraces uncertainty instead of faking a precision no team actually has; humans are
better at "bigger or smaller than this" than at absolute duration prediction. Velocity (points
completed per sprint, averaged over several sprints) turns relative sizes into a forecast: divide
remaining backlog points by average velocity.

</details>

**Q6 (co-06 -- planning-poker-pitfalls).** Name the two biases planning-poker facilitation rules
counter, and the rule that neutralizes each.

<details>
<summary>Answer</summary>

Anchoring, neutralized by a blind simultaneous reveal (no spoken number can pull anyone else's
guess). Authority bias, neutralized by having the highest and lowest estimators explain their
reasoning first when estimates diverge, rather than deferring automatically to the most senior
voice.

</details>

**Q7 (co-07 -- sprint-and-backlog-planning).** What two conditions must a sprint plan satisfy to be
well-formed?

<details>
<summary>Answer</summary>

Committed points must never exceed the team's known velocity, and no task in the plan may precede a
dependency that is not itself scheduled in an earlier sprint.

</details>

**Q8 (co-08 -- execution-mechanics).** What should a good standup structurally surface, and why does
a WIP limit matter?

<details>
<summary>Answer</summary>

Blockers, not a chronological status recitation. A WIP limit caps how many items one workflow stage
can hold at once, forcing attention onto finishing started work rather than starting more -- and
both mechanisms exist to move the moment a problem is discovered as early as possible.

</details>

**Q9 (co-09 -- metrics).** What test must a metric pass to earn a place on a dashboard?

<details>
<summary>Answer</summary>

A one-sentence "when this metric shows X, we do Y" decision rule must be writable for it. A metric
with no such rule is decoration and should be dropped.

</details>

**Q10 (co-10 -- risk-management).** What four things does a well-formed risk register entry have?

<details>
<summary>Answer</summary>

A likelihood rating, an impact rating, a computed likelihood-times-impact score, a mitigation
specific enough to act on (not "monitor closely"), and a named owner accountable for that
mitigation.

</details>

**Q11 (co-11 -- change-management).** What must a change-request decision state explicitly, beyond
simply "approved" or "denied"?

<details>
<summary>Answer</summary>

What the triple constraint absorbs -- what is dropped, delayed, or funded -- to accommodate the
change, run through an explicit accept/defer/trade decision rather than slipping in silently.

</details>

**Q12 (co-12 -- retrospectives).** What must every action a retrospective produces have to count as
well-formed?

<details>
<summary>Answer</summary>

A named owner and a measurable done-signal -- something checkable next sprint, not a vague
intention.

</details>

**Q13 (co-13 -- stakeholder-communication).** What must every row of a stakeholder communication
plan name, beyond cadence and format?

<details>
<summary>Answer</summary>

The specific decision that update is meant to drive -- reprioritize, fund a mitigation, adjust a
date, approve a change -- not merely what information the update contains.

</details>

**Q14 (co-14 -- goodhart-metric-abuse).** State Goodhart's Law and its canonical failure mode in
delivery work.

<details>
<summary>Answer</summary>

"When a measure becomes a target, it stops being a good measure." In delivery work: the instant a
team's velocity is used to judge or rank its productivity, the team gains a direct incentive to
inflate point estimates -- same actual work, a bigger declared number, and the number now lies to
everyone who relies on it for forecasting.

</details>

**Q15 (co-15 -- process-weight-fit).** What formula gives a team's communication-path count, and why
does it mean ceremony cannot be a fixed package regardless of team size?

<details>
<summary>Answer</summary>

`n(n-1)/2`, quadratic in team size. Because coordination cost scales with that quadratic curve while
a fixed ceremony package's cost is roughly flat per person, the "right size" of process genuinely
differs by team size -- a package barely-there on an eight-person team can dominate a two-person
team's week.

</details>

## Applied scenarios

Eleven scenarios. Each is self-contained -- everything you need is in the prompt itself, no other
page required. Decide which concept and which move applies, then check.

**AS1.** A nonprofit's fundraising platform must launch before a fixed grant deadline, deliver every
feature the grant proposal listed, and stay within a budget that is already fully spent. The
program director insists all three are non-negotiable. What is wrong with this request, and what
should the team's first move be?

<details>
<summary>Answer</summary>

This is the impossible ask co-01 warns against: fixing scope, schedule, and cost simultaneously is
not a plan. The team's first move is not to attempt all three -- it is to force an explicit
conversation about which two are genuinely fixed (the grant deadline almost certainly is; the
already-spent budget likely is too) and get an honest answer about what the third -- scope -- must
absorb, in writing, before any work begins.

</details>

**AS2.** A game studio's live-ops team patches a shipped game continuously based on daily
player-behavior telemetry, with new priorities arriving unpredictably as issues are discovered.
Which methodology fits, and why?

<details>
<summary>Answer</summary>

Kanban. Work arrives continuously and unpredictably from telemetry, with no natural
sprint-length iteration boundary to plan two weeks of it around -- exactly the property co-02 names
as Kanban's fit, not Scrum's fixed-cadence reprioritization or waterfall's locked-plan approach.

</details>

**AS3.** A WBS leaf reads simply "Backend work" and is meant to cover a checkout endpoint change, a
notification-service change, and an auth-service session change. What is wrong with this leaf, and
what should replace it?

<details>
<summary>Answer</summary>

It fails co-03's independently-estimable-and-assignable test: it spans three unrelated services with
no single owner, so nobody can size it with confidence or take end-to-end ownership of it. It should
be decomposed into three separate leaves, one per service, each assignable to a single owner.

</details>

**AS4.** A small dependency graph: Task A (2 days) has no prerequisite. Task B (5 days) depends on
A. Task C (3 days) depends on A. Task D (2 days) depends on both B and C. Compute the critical path.

<details>
<summary>Answer</summary>

Two paths reach D: A -> B -> D = 2+5+2 = 9 days, and A -> C -> D = 2+3+2 = 7 days. The critical path
is A -> B -> D at 9 days, with zero slack; A -> C -> D carries 2 days of slack (C could run 2 days
long before it affects D's start).

</details>

**AS5.** A team debates estimating in hours "because it's more precise" instead of story points.
What is the flaw in that reasoning?

<details>
<summary>Answer</summary>

An hour estimate claims a confidence the team does not actually have at the start of a task -- it
looks precise without being accurate. Story points sidestep this by asking only "bigger or smaller
than this reference," a comparison humans are demonstrably better at than absolute duration
prediction (co-05); the apparent precision of hours is the flaw, not a feature.

</details>

**AS6.** In planning-poker sessions, the tech lead always reveals their card first and explains their
reasoning before anyone else votes. Which bias is this, and what facilitation fix addresses it?

<details>
<summary>Answer</summary>

Authority bias -- the tech lead's number becomes the anchor everyone else defers to rather than one
opinion among several. The fix is a blind, simultaneous reveal (co-06): every participant locks in a
card privately before anyone's number is visible to anyone else.

</details>

**AS7.** A team's dashboard tracks six metrics: burndown, cycle time, lead time, lines of code
committed per day, number of Slack messages in the team channel, and meeting-attendance rate. Which
of these fail co-09's test, and why?

<details>
<summary>Answer</summary>

Lines of code committed per day, Slack message count, and meeting-attendance rate all fail: none has
a stated "when this shows X, we do Y" decision attached, and none of the three obviously maps to one
either (more commits or more messages does not clearly call for any specific action). Burndown,
cycle time, and lead time each pass, because each already has a concrete decision co-09's worked
scenario mapped to it.

</details>

**AS8.** A risk register entry reads: "Risk: third-party API might change. Likelihood 3, Impact 4,
Score 12. Mitigation: monitor closely. Owner: team." What is wrong with this entry, and how would
you rewrite the mitigation?

<details>
<summary>Answer</summary>

"Monitor closely" is not a concrete, actionable mitigation -- it describes an intention, not a
committed action, and "team" is not a named individual accountable for it. A concrete rewrite: "Pin
the API's SDK version, subscribe to the vendor's changelog, and smoke-test weekly against their
sandbox environment," with a single named owner (co-10).

</details>

**AS9.** Two weeks into a sprint, a stakeholder emails "can you just also add X, it's small" with no
further discussion. What should the team's response be, per co-11?

<details>
<summary>Answer</summary>

Route it through an explicit accept/defer/trade decision against the triple constraint, not
silently squeeze it in. The response should state what X's addition would cost -- a schedule slip, a
dropped lower-priority item, or added budget -- and let the stakeholder choose, rather than
absorbing it invisibly.

</details>

**AS10.** A VP proposes: "let's pay a bonus multiplier based on total story points shipped per
quarter, to reward our fastest teams." What failure mode does this trigger, and what would happen to
the team's own forecasting as a result?

<details>
<summary>Answer</summary>

Goodhart's Law (co-14): the moment points shipped affects compensation, teams gain a direct
incentive to inflate estimates -- identical work, bigger declared numbers. This also destroys the
number's original, legitimate use: the team's own historical velocity becomes meaningless for
forecasting (co-05) once it has been inflated to chase the bonus.

</details>

**AS11.** A 15-person team runs with no formal ceremony at all ("we just talk when we need to"),
while a 3-person team runs the exact same heavyweight ceremony package as the 15-person team (daily
standup, full sprint planning, biweekly retro, cross-team sync). Diagnose both mismatches.

<details>
<summary>Answer</summary>

The 15-person team has `15*14/2 = 105` communication paths -- far too many for ad hoc "talk when we
need to" coordination to actually cover; without structured ceremony, work will silently drift out
of sync across most of those 105 paths. The 3-person team has only `3*2/2 = 3` paths; the identical
heavyweight package is wildly oversized for that little coordination surface and consumes a
disproportionate share of a 3-person team's week for coordination need that does not exist (co-15).
Both are process-weight mismatches, in opposite directions.

</details>

## Artifact recreation drills

Seven before/after decision-artifact drills. Each gives a flawed, self-contained mocked artifact --
spot and fix the flaw yourself, then compare against the "after" version and its root-cause
explanation.

### Drill 1 -- risk register missing an owner column

**Before**:

| Risk                              | Likelihood | Impact | Score | Mitigation                     |
| --------------------------------- | ---------- | ------ | ----- | ------------------------------ |
| Vendor API deprecated mid-project | 3          | 4      | 12    | Monitor the vendor's changelog |

<details>
<summary>Model fix and root cause</summary>

**After**:

| Risk                              | Likelihood | Impact | Score | Mitigation                                                                                     | Owner             |
| --------------------------------- | ---------- | ------ | ----- | ---------------------------------------------------------------------------------------------- | ----------------- |
| Vendor API deprecated mid-project | 3          | 4      | 12    | Pin the SDK version; subscribe to the vendor's changelog; budget one sprint of migration slack | Integrations lead |

**Root cause**: a risk with a mitigation but no named owner is not actually being managed -- nobody
is accountable for doing the mitigation, so it competes with everyone's other priorities and loses
by default. co-10 requires all four fields: likelihood, impact, score, mitigation, _and_ a named
owner.

</details>

### Drill 2 -- WBS leaf that isn't independently assignable

**Before**:

```text
2.0 Platform Work
  2.1 Backend work (payments, notifications, and auth changes)
```

<details>
<summary>Model fix and root cause</summary>

**After**:

```text
2.0 Platform Work
  2.1 Payments service: checkout endpoint change
  2.2 Notifications service: delivery API change
  2.3 Auth service: session-refresh change
```

**Root cause**: "Backend work" spans three unrelated services with no single owner or skill area --
it fails co-03's independently-estimable-and-assignable test. Splitting it by service produces three
leaves a team member can size and own individually.

</details>

### Drill 3 -- dependency graph missing an edge

**Before**: a project's dependency graph lists "Design review" (3 days) and "Implementation" (6
days) as two independent tasks with no edge between them, both starting on day 1. The computed
critical path is `Implementation (6 days)` alone.

<details>
<summary>Model fix and root cause</summary>

**After**: add the missing edge, `Design review -> Implementation` (implementation cannot
meaningfully start before the design is reviewed and approved). The critical path recalculates to
`Design review -> Implementation = 3 + 6 = 9 days`, three days longer than the flawed original.

**Root cause**: an omitted real "must finish before" relation implicitly claims two tasks can run in
parallel when they cannot -- co-04 requires every genuine precedence relation to be encoded as an
edge. Missing even one edge on the true critical path understates the schedule and sets the project
up to commit to a date it cannot actually hit.

</details>

### Drill 4 -- sprint plan that over-commits capacity

**Before**: team velocity is 20 points/sprint (three-sprint average). The sprint plan commits:
Task A (10), Task B (8), Task C (8) -- 26 points total.

<details>
<summary>Model fix and root cause</summary>

**After**: commit Task A (10) and Task B (8) -- 18 points, under the 20-point ceiling. Defer Task C
(8 points) to the next sprint.

**Root cause**: co-07 requires committed points to never exceed known velocity. A 26-point
commitment against a 20-point velocity sets the team up to either work unsustainable hours or ship a
broken promise -- the fix is to cut the lowest-priority item, not to hope the team beats its own
historical average.

</details>

### Drill 5 -- standup that stays status theater

**Before**: a daily standup is a round-robin where each person says "yesterday I worked on X, today
I'll work on Y, no blockers" -- while one person's card has visibly not moved on the board for four
days.

<details>
<summary>Model fix and root cause</summary>

**After**: walk the board right-to-left, closest-to-done first; ask exactly two questions per card --
"is this blocked?" and "has this been sitting longer than two days?" -- rather than asking each
person to self-report.

**Root cause**: self-reporting depends on someone recognizing their own situation as "blocked,"
which the four-day-stuck card shows doesn't reliably happen. Asking a fixed diagnostic question per
card, board-driven rather than person-driven, catches exactly what self-report missed (co-08).

</details>

### Drill 6 -- communication matrix row with no named decision

**Before**:

| Audience       | Cadence | Format       |
| -------------- | ------- | ------------ |
| Marketing team | Weekly  | Email update |

<details>
<summary>Model fix and root cause</summary>

**After**:

| Audience       | Cadence | Format       | Decision it drives                                                                          |
| -------------- | ------- | ------------ | ------------------------------------------------------------------------------------------- |
| Marketing team | Weekly  | Email update | Whether to adjust the public launch-messaging timeline based on current schedule confidence |

**Root cause**: an update with no attached decision is status theater regardless of audience --
co-13 requires every row to name what actually changes, for someone, as a result of that update.

</details>

### Drill 7 -- velocity forecast using a single best sprint

**Before**: the last three sprints' velocity was 14, 16, and 22 points. The forecast for a
remaining 66-point backlog uses the most recent sprint's 22-point velocity: 66 / 22 = 3 sprints.

<details>
<summary>Model fix and root cause</summary>

**After**: use the three-sprint average, (14 + 16 + 22) / 3 = 17.3, rounded down to 17 for
conservative planning: 66 / 17 = 3.9, rounded up to **4 sprints**.

**Root cause**: cherry-picking the best of three sprints produces an overly optimistic forecast --
co-05 requires an average of at least three sprints specifically so one unusually good (or bad)
sprint cannot dominate the number the team commits a stakeholder-facing date to.

</details>

## Self-check checklist

Confirm each item without checking the concepts page first. If you hesitate, that concept needs
another pass.

- [ ] I can name the two constraints a trade-off memo must hold fixed and state what the third
      absorbs, in one sentence. (co-01)
- [ ] I can match a delivery context to waterfall, Scrum, or Kanban and name the specific property
      that drives the choice. (co-02)
- [ ] I can decompose a deliverable into WBS leaves that are each independently estimable and
      independently assignable. (co-03)
- [ ] I can compute a critical path by summing durations along every path and identifying the
      longest one with zero slack. (co-04)
- [ ] I can size a backlog item relative to a reference story and forecast completion from a
      multi-sprint velocity average, never a single sprint's number. (co-05)
- [ ] I can name which bias -- anchoring or authority bias -- a given planning-poker facilitation
      rule neutralizes. (co-06)
- [ ] I can build a sprint plan that never exceeds velocity and never violates dependency order.
      (co-07)
- [ ] I can redesign a status-theater standup into one that structurally surfaces blockers and WIP.
      (co-08)
- [ ] I can write a one-sentence decision rule for a metric, or explain why a metric with none
      should be dropped. (co-09)
- [ ] I can build a risk register entry with a computed score, a concrete mitigation, and a named
      owner. (co-10)
- [ ] I can write a change-request decision that states exactly what the triple constraint absorbs.
      (co-11)
- [ ] I can turn raw retrospective observations into actions with a named owner and a measurable
      done-signal. (co-12)
- [ ] I can build a stakeholder communication plan where every row names the decision it drives.
      (co-13)
- [ ] I can explain Goodhart's Law's specific failure mode for velocity, and propose an outcome
      metric that resists it. (co-14)
- [ ] I can compute a team's communication-path count (`n(n-1)/2`) and use it to right-size ceremony.
      (co-15)
- [ ] I can explain, in one sentence, why a story-point estimate or a risk score is an honest
      decision under uncertainty rather than a prediction to be graded later. (`correctness-vs-pragmatism`)
- [ ] I can explain, in one sentence, why a task's zero slack on the critical path is a form of
      coupling, and why a low-cohesion WBS leaf resists estimation. (`coupling-vs-cohesion`)

## Elaborative interrogation and self-explanation

Six why/why-not prompts, tied to this topic's two Cross-Cutting Big-Idea tags. Answer each in your
own words before opening the model explanation.

**E1 (`correctness-vs-pragmatism`).** Why does this topic insist a story-point estimate is a
decision made under uncertainty rather than a prediction to be graded against actual hours spent
later? What would be lost if a team graded estimates that way?

<details>
<summary>Model explanation</summary>

co-05 and co-10 both replace an impossible demand -- predict the future precisely -- with an honest
one: commit to the most defensible number available right now, given genuine uncertainty. Grading an
estimate against actual hours after the fact treats it as if it were a prediction, which punishes
honest uncertainty and teaches the team to pad future estimates defensively -- exactly the
Goodhart-style distortion co-14 names for velocity used as a performance target. Pragmatism means the
number stays useful for its actual purpose (relative sizing, forecasting) precisely because it was
never asked to be "correct" in an after-the-fact sense.

</details>

**E2 (`correctness-vs-pragmatism`).** co-01's triple constraint says "pick two fixed, the third
absorbs" -- why is this framed as a pragmatic discipline instead of a search for the mathematically
correct trade-off?

<details>
<summary>Model explanation</summary>

There is no single correct trade-off computable from first principles -- the right trade depends on
the specific stakes of a specific project (a fixed grant deadline versus a flexible internal tool),
which is a judgment call, not a calculation. What co-01 actually teaches is not "compute the right
answer" but "make the trade-off explicit and owned." Pragmatism here replaces an impossible search
for one objectively correct answer with an honest, visible, chosen one -- the discipline is in the
naming, not in the arithmetic.

</details>

**E3 (`correctness-vs-pragmatism`).** If the final story-point value is ultimately just whatever the
team agrees on, why does co-06's planning-poker facilitation process matter at all?

<details>
<summary>Model explanation</summary>

Because agreement reached through anchoring or authority bias is not actually the team's honest
judgment -- it is one person's judgment the rest are quietly deferring to. There is no objectively
correct point value for a team to converge on, only a more or less honest one; the facilitation
rules exist to make the eventual agreed number pragmatically closer to what the team collectively,
honestly believes, which is the only kind of "correct" available here.

</details>

**E4 (`coupling-vs-cohesion`).** Why does this topic describe the critical path (co-04) as "the
tightest chain of coupling" rather than simply "the longest sequence of tasks"?

<details>
<summary>Model explanation</summary>

Coupling, in code, means one component cannot change independently of another. On a project
schedule, a task with zero slack is coupled to the project's finish date in exactly that sense: you
cannot delay it without delaying everything downstream of it. Framing the critical path as coupling,
not merely "long," is what makes co-04's actionable insight visible -- expedite the coupled chain
specifically, not just whichever piece of work looks biggest.

</details>

**E5 (`coupling-vs-cohesion`).** A WBS leaf (co-03) must be independently estimable and assignable --
how does that connect to cohesion, and what happens to a leaf that fails the test?

<details>
<summary>Model explanation</summary>

A leaf that is independently estimable and assignable is, by definition, cohesive -- it is one
coherent unit of work, not several unrelated concerns bundled together. A leaf like "backend work"
spanning three unrelated services is low-cohesion: it bundles unrelated concerns, which is exactly
why it resists being sized or owned by one person (Drill 2). Decomposing it into cohesive leaves is
the project-management equivalent of decomposing a low-cohesion module into focused ones.

</details>

**E6 (`coupling-vs-cohesion`).** Why does co-15's process-weight-fit argument (`n(n-1)/2`
communication paths) belong under coupling-vs-cohesion rather than under execution mechanics
(co-08)?

<details>
<summary>Model explanation</summary>

Every communication path is a coupling between two team members -- a channel through which one
person's work can silently drift out of sync with another's unless something actively holds it
together. As team size grows, the number of these couplings grows quadratically, which is exactly
why ceremony has to scale non-linearly too. This is a structural coupling argument about the team
itself, distinct from co-08's separate concern (which mechanisms make in-flight work visible day to
day) -- co-15 is about how much of that mechanism a team's actual coupling structure needs in the
first place.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
