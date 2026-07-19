---
title: "Beginner Scenarios"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 10
---

Scenarios 1-9 establish the single-decision discipline every later scenario in this topic builds
on: running a report-owned 1:1, writing SBI feedback (both reinforcing and corrective), coaching
instead of directing, sketching a growth plan, mapping behavior to a competency ladder, delegating
with context, and naming the IC-to-manager transition and the manager-vs-maker tension in plain
language. Most scenarios follow **Everline**, a fictional B2B SaaS analytics company, and its
Platform team manager, **Priya Kapoor** -- every name, quote, and "the team said" line below is an
illustrative, constructed example written to teach the technique, not a real transcript. Every
artifact below also lives, standalone, under `learning/artifacts/`.

---

### Worked Scenario 1: First 1:1 Agenda

**Context**: Exercises co-02. Noor Rahman just joined Everline's Platform team. Priya drafts the
recurring 1:1 agenda template they will use going forward, flipping the traditional
manager-runs-the-meeting format.

**Decision artifact**:

> **Weekly 1:1 -- Priya & Noor**
>
> **Noor's agenda (fill in before the meeting, in any order):**
>
> 1. Anything blocking you right now?
> 2. Anything on your mind about the team, the work, or your own growth?
> 3. Anything you want feedback on?
>
> **Priya's agenda (only added after Noor's items are covered):**
>
> 1. One thing I want to flag or ask about this week.
>
> **Standing note**: if Noor's list is empty some week, that's fine -- the meeting still starts by
> asking, not by Priya filling the silence with a status update.

**Verify**: Noor's items (1-3) are listed and worked through first; Priya's own item (4) is
explicitly gated on Noor's list being covered first -- satisfying co-02's rule that a report-owned
1:1 puts the report's agenda ahead of the manager's.

**Key takeaway**: The template doesn't ban Priya from raising her own topics -- it just sequences
them last, so the meeting can't quietly turn into Priya's status check dressed up as Noor's 1:1.

**Why It Matters**: A 1:1 that a manager runs top-to-bottom trains the report to show up with
nothing prepared, because nothing they'd bring ever gets asked for first -- over a few months, that
silently closes the one recurring channel built specifically for things too sensitive or too
half-formed for a group meeting.

---

### Worked Scenario 2: SBI Feedback, Positive

**Context**: Exercises co-03. Jordan, a senior engineer on the Platform team, caught a data-quality
bug in production before it reached customers and drove the fix personally. Priya writes SBI
feedback rather than a generic "great job."

**Decision artifact**:

> **Situation**: During Tuesday's deploy of the new currency-conversion service, you noticed the
> staging smoke test's output looked one decimal place off, even though the test itself passed.
>
> **Behavior**: You paused the rollout, traced the discrepancy to a silent floating-point rounding
> difference between the staging and production currency tables, and wrote a fix plus a
> regression test before resuming the deploy -- about 40 minutes added to the rollout.
>
> **Impact**: That 40 minutes prevented a currency-rounding bug from reaching every customer
> invoice generated that week -- the kind of bug that's expensive and embarrassing to unwind after
> the fact, and nearly invisible if it ships quietly.

**Verify**: the note names the specific situation (Tuesday's currency-service deploy), the observed
behavior (paused the rollout, traced the discrepancy, wrote a fix and a regression test), and the
impact (prevented a customer-facing invoice bug) -- not a general "great job," satisfying co-03's
rule.

**Key takeaway**: Nothing in the note says "you're a careful engineer" -- it says what Jordan did,
in this one situation, and what it prevented. That's what makes it repeatable: Jordan now knows
exactly which behavior to do again next time something looks slightly off.

**Why It Matters**: "Great catch, thanks!" would have felt nice for five seconds and taught Jordan
nothing about which specific instinct to trust next time -- the SBI version turns one good moment
into a habit Jordan can consciously repeat, and it gives Priya a specific, evidenced data point she
can cite later in a calibration conversation, instead of a vague, unsupported impression.

---

### Worked Scenario 3: SBI Feedback, Corrective

**Context**: Exercises co-03. Sam, an engineer on the Platform team, missed the agreed deadline for
the schema-migration script by three days with no advance warning. Priya writes corrective SBI
feedback.

**Decision artifact**:

> **Situation**: The schema-migration script was due Monday for Wednesday's release; it landed
> Thursday, and I found out it was late from the release checklist, not from you.
>
> **Behavior**: You didn't flag the slip when you first noticed you were behind, sometime around
> Friday of the prior week based on your commit history -- the deadline just quietly passed.
>
> **Impact**: The release had to be delayed a day, and I had to explain the delay to the product
> team without being able to say why it happened, because I didn't know either.
>
> **Instead**: Next time you're behind on a committed date, flag it the day you notice, even before
> you have a fix -- "I'm going to miss Monday, here's why, here's my new estimate" costs you thirty
> seconds and lets me manage the release plan around it instead of around a surprise.

**Verify**: the note stays behavior-focused ("you didn't flag the slip," not "you're unreliable")
and states the specific "instead" wanted going forward (flag a slip the day it's noticed) --
satisfying co-03's rule for corrective feedback.

**Key takeaway**: The feedback never says Sam is a bad engineer -- it says one specific thing Sam
did (stayed silent about slipping) and one specific thing to do differently next time (flag it
early). That distinction is what keeps Sam able to hear it without getting defensive.

**Why It Matters**: "You need to be more reliable" gives Sam nothing to actually change -- the SBI
version gives Sam one concrete action (flag slips early) that directly prevents the exact failure
that happened this time, and it gives Priya a documented, specific basis to return to if the same
pattern shows up again next month instead of relitigating it from scratch.

---

### Worked Scenario 4: Coaching Question vs Answer

**Context**: Exercises co-04. Alex, an engineer on the Platform team, is stuck deciding whether the
new event-ingestion service should validate incoming events synchronously or push invalid events to
a dead-letter queue for later inspection. Priya drafts both a directive answer and a coaching
version.

**Decision artifact**:

> **Directive version (what NOT to lead with)**: "Use a dead-letter queue -- synchronous validation
> will add latency to the ingestion path and you don't want that on the hot path."
>
> **Coaching version (what Priya actually sends)**:
>
> 1. What happens to an event today if it fails validation -- where does it go, and who notices?
> 2. If you delay the validation to a background process instead of the ingestion path itself, what
>    does the ingestion path gain, and what does it lose?
> 3. Who's the audience for "an event failed validation" -- is it a human who needs to fix bad data,
>    an alert that needs to fire immediately, or both?

**Verify**: the coaching version supplies no solution -- it contains three questions and zero
statements of what Alex should do -- satisfying co-04's rule that a coaching response, unlike a
directive one, gives no answer.

**Key takeaway**: The directive version would have solved today's ticket in one sentence. The
coaching version costs more of Priya's time up front, but Alex is the one who reasons through the
latency/visibility trade-off -- next time a similar validation-placement question comes up, Alex has
already practiced the reasoning, not just received the conclusion.

**Why It Matters**: If Priya always gives the answer, every future version of this same question
still routes through Priya -- coaching is slower once, but it's the only path that gets Alex to a
place where Priya isn't the bottleneck on this class of decision anymore.

---

### Worked Scenario 5: Growth Plan Artifact

**Context**: Exercises co-05, co-06. Maya, an engineer on the Platform team, wants to grow toward
Senior Engineer. Priya drafts a growth plan naming strengths, gaps, and next-level behaviors.

**Decision artifact**:

> **Growth plan -- Maya, Engineer -> Senior Engineer**
>
> **Strengths (keep doing)**: ships reliably within estimate on well-scoped tasks; writes tests that
> actually catch the bugs she's worried about, not just tests that pass.
>
> **Gaps mapped to next-level behaviors**:
>
> - **Gap**: doesn't yet propose the technical approach before starting work -- waits to be told the
>   design. **Next-level behavior** (per the Senior Engineer ladder rung): "proposes a design
>   approach for a multi-day task before writing code, and can defend a trade-off in it."
> - **Gap**: rarely reviews other engineers' PRs unless assigned. **Next-level behavior**: "reviews
>   at least 2-3 PRs a week beyond assigned ones, catching design issues, not just style."
>
> **Next step**: for the next task-sized project, Maya writes a one-page design note before coding
> and brings it to a 1:1 for feedback -- practicing the exact next-level behavior named above.

**Verify**: both named gaps map to an observable behavior quoted from the Senior Engineer ladder
rung (proposing a design approach with a defensible trade-off; reviewing PRs beyond assigned ones),
not a vague trait like "needs more leadership" -- satisfying co-05 and co-06's rule.

**Key takeaway**: "Be more senior" would have told Maya nothing actionable. This plan tells her
exactly two things to start doing, each one directly lifted from the ladder's own language, so
there's no ambiguity about what "next level" actually means in practice.

**Why It Matters**: A growth plan that stays at the level of "shows more initiative" leaves the
report guessing what that even looks like day to day -- naming the exact behavior (write the design
note, review the PRs) gives Maya something she can start doing this week, not a mood to somehow
embody.

---

### Worked Scenario 6: Ladder Behavior Mapping

**Context**: Exercises co-06. Priya reviews three of Maya's recent actions against the Senior
Engineer ladder rung to confirm the growth plan's gaps are grounded in the ladder's actual text, not
just Priya's impression.

**Decision artifact**:

> | Maya's recent action                                                                                                                                 | Ladder rung cited                                                                                        | Meets it?                                                                          |
> | ---------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- |
> | Wrote a one-page design note for the event-retry logic before coding it, and defended the choice of exponential backoff over fixed retry in her 1:1. | "Proposes a design approach for a multi-day task before writing code, and can defend a trade-off in it." | Yes -- first time this quarter.                                                    |
> | Reviewed 1 PR this week, only because Priya assigned it directly.                                                                                    | "Reviews at least 2-3 PRs a week beyond assigned ones, catching design issues, not just style."          | Not yet -- volume and initiative both short of the rung.                           |
> | Caught a subtle off-by-one in a teammate's PR during that one assigned review, with a specific suggested fix.                                        | (Same PR-review rung as above)                                                                           | Partial -- when she does review, the depth is already there; frequency is the gap. |

**Verify**: each row cites the ladder's own stated behavior text verbatim (in quotes) as the
standard being checked against, not Priya's subjective impression of what "senior enough" looks
like -- satisfying co-06's rule.

**Key takeaway**: The table shows Maya is already capable of the depth the ladder asks for (the
off-by-one catch) -- what's missing is frequency and initiative, not skill. That's a more precise,
more encouraging diagnosis than a vague "needs to review more."

**Why It Matters**: Without mapping to the ladder's actual text, "Maya's not quite senior yet" is
an opinion Maya can't act on or contest. Mapped to specific quoted behaviors, it becomes a checklist
both Priya and Maya can independently verify against the same evidence.

---

### Worked Scenario 7: Delegation Context Brief

**Context**: Exercises co-08. Priya wants Jordan to choose and implement a caching strategy for the
event-ingestion service's lookup table, without Priya dictating the specific approach.

**Decision artifact**:

> **Delegation brief -- lookup-table caching, owner: Jordan**
>
> **What**: the lookup table gets read on every ingested event and is currently a database round
> trip each time; we need this to stop being the ingestion path's slowest step.
>
> **Why**: the event-ingestion service's p95 latency budget is 150ms end to end, and the lookup
> query alone currently averages 80ms under peak load -- that's over half the budget on one step.
> The lookup table itself changes rarely (a few times a day at most).
>
> **Constraints that matter**: whatever you choose has to tolerate the lookup table changing
> without ingestion serving stale data for more than a few minutes, and it can't add a new
> infrastructure dependency the team doesn't already operate (no new cache cluster to run on-call
> for).
>
> **Not specified on purpose**: whether that's an in-process cache with a TTL, a write-through cache
> keyed on table version, or something else -- that choice is yours; bring it to Thursday's 1:1 if
> you want a second opinion before committing.

**Verify**: a reader unfamiliar with Priya's own private preference could still reach the same
constraint-respecting decision from the brief alone -- the what (stop the round trip), the why (the
latency budget), and the real constraints (staleness tolerance, no new infra dependency) are all
stated in writing; the specific caching mechanism is deliberately absent -- satisfying co-08's rule.

**Key takeaway**: Priya almost certainly has a caching approach in mind, but she doesn't write it
down -- what she writes down is everything Jordan needs to arrive at a good answer independently,
including the constraints that would rule out a bad one.

**Why It Matters**: A brief that only said "add caching to the lookup table" would leave Jordan
guessing at the actual constraint that matters (staleness tolerance, no new infra) -- and a brief
that instead specified the exact caching mechanism would have skipped the point of delegating in the
first place.

---

### Worked Scenario 8: IC-to-Manager Mindset Memo

**Context**: Exercises co-01. Priya was promoted from senior engineer to manager of the Platform
team two weeks ago. She writes a first-week memo to herself naming what she's stopping and what
replaces it.

**Decision artifact**:

> **What I'm stopping**: personally taking the hardest, most interesting tickets in every sprint
> planning session -- for years, that was the fastest way for me to add value, and it's the reflex
> I have to consciously override now. I'm also stopping being the default code reviewer on every
> pipeline-critical PR; I was the fastest reviewer on the team, but that made me a bottleneck nobody
> could see until I was out sick for two days last month and three PRs sat untouched.
>
> **What replaces it**: instead of taking the hard ticket myself, I name who on the team is closest
> to ready for it and pair with them on the design, not the implementation. Instead of reviewing
> every pipeline-critical PR myself, I'm asking Jordan and Maya to be the primary reviewers for that
> path, and I review their reviews occasionally, not the code directly.

**Verify**: the memo names concrete IC habits given up (taking the hardest tickets personally,
being the default reviewer on critical PRs) and the specific practice replacing each one (naming a
ready teammate and pairing on design; delegating primary review), not just an aspiration like "I'll
delegate more" -- satisfying co-01's rule.

**Key takeaway**: The memo doesn't just say "I'll be a better manager" -- it names two specific,
previously-rewarded IC habits and states exactly what replaces each one, so Priya has something
concrete to catch herself doing wrong next week.

**Why It Matters**: The habits that made Priya a great senior engineer -- taking the hard problems,
being the fastest reviewer -- are precisely the habits that, unexamined, would make her a bottleneck
as a manager; naming them explicitly is what makes them possible to actually stop.

---

### Worked Scenario 9: Manager-vs-Maker Catch

**Context**: Exercises co-20, co-01. Three months into managing, Priya has a bad week: she wrote
most of a critical pipeline fix herself under deadline pressure and missed two scheduled 1:1s
because of it. She diagnoses what happened.

**Decision artifact**:

> **What happened**: a production data-quality incident hit Thursday morning. Instead of assigning
> it and coaching from the side, I opened the code myself and fixed it directly -- it was faster in
> the moment, and I was the person who knew the ingestion pipeline best. I then spent Friday
> finishing the fix's test coverage myself instead of handing it off, and cancelled both Thursday
> and Friday 1:1s to do it.
>
> **The bottleneck this created**: nobody else on the team got closer to being able to handle the
> next pipeline incident alone -- I was, again, the single person who could diagnose and fix this
> class of bug fastest, which is exactly the bottleneck my promotion was supposed to remove. Two
> reports also went a full extra week without their 1:1, right when one of them (Sam, per Worked
> Scenario 3) needed a follow-up on a feedback conversation.
>
> **Corrective habit change**: for the next production incident, I pair with whoever's closest to
> ready on that part of the system and narrate my diagnosis out loud instead of silently fixing it
> -- slower during the incident itself, but it's the only path that makes the team less dependent on
> me being available next time. 1:1s move only if the report agrees, never unilaterally.

**Verify**: the diagnosis names the specific bottleneck created (Priya remains the single fastest
diagnostician, no one else grew closer to handling it alone) and one corrective habit change
(pair and narrate instead of silently fixing; never unilaterally cancel a 1:1) -- satisfying
co-20 and co-01's rule.

**Key takeaway**: The incident itself got fixed either way -- the real cost wasn't Thursday's
outage, it was that the team ended the week no more capable of handling the next one without Priya
than it started, and two people's trust-building time got quietly sacrificed to buy that speed.

**Why It Matters**: "I was just being helpful" is the easiest story to tell about a manager-vs-maker
slip, because in the moment it always feels efficient -- the corrective habit only sticks if the
manager can name, in writing, exactly what independence the team lost by not doing it the slower
way.

---

← Previous: [Overview](./overview.md) · Next: [Intermediate Scenarios](./intermediate.md) →
