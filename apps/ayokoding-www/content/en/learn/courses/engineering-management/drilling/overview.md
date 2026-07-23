---
title: "Overview"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Engineering Management topic: recall first,
then applied judgment, then hands-on artifact repair, then a checklist to confirm real
automaticity, and finally why/why-not prompts that test whether you can explain the reasoning, not
just produce the artifact. Every answer is hidden in a `<details>` block; try each item yourself
before opening it.

This topic has no runnable interpreter -- every drill below is a decision-artifact repair drill
instead of a code fix, verified the same observable-property way this topic's worked scenarios were
verified (checking a stated element is present, matching a claim against a stated rule), not by
running anything. Every scenario or artifact below is self-contained and illustrative -- Everline is
a fictional company, and no quoted number or conversation is a real transcript.

## Recall Q&A

Twenty short-answer questions, one per concept (`co-01` through `co-20`). Answer from memory, then
check.

**Q1 (co-01 -- ic-to-manager-transition).** What is the core change in what a manager does compared
to being an IC, and why is that change hard to unlearn?

<details>
<summary>Answer</summary>

The job changes from personally solving problems to building a team that solves them -- the new
scarce resource is other people's judgment, not the manager's own output. It's hard to unlearn
because the exact IC behaviors (personally shipping, personally fixing) were rewarded for years and
don't disappear automatically just because a title changed.

</details>

**Q2 (co-02 -- one-on-ones).** What must a report-owned 1:1 agenda's ordering look like?

<details>
<summary>Answer</summary>

The report's items are listed and worked through first; any manager item is explicitly added only
after the report's own agenda is exhausted -- not a status update the manager runs top-to-bottom.

</details>

**Q3 (co-03 -- feedback-sbi).** What three elements does SBI feedback require, and what must it
avoid?

<details>
<summary>Answer</summary>

Situation, Behavior, and Impact -- a specific event, an observed (not inferred) action, and its
stated effect. It must avoid trait or character language ("you're careless") in favor of
behavior language ("in this situation, this specific thing happened").

</details>

**Q4 (co-04 -- coaching-vs-directing).** What test distinguishes a coaching response from a
directive one?

<details>
<summary>Answer</summary>

A coaching response supplies only questions, no answer; scan it for any sentence stating what the
report should do -- if one exists, it's directing, not coaching.

</details>

**Q5 (co-05 -- growth-plans).** What must every gap named in a growth plan map to?

<details>
<summary>Answer</summary>

An observable behavior tied to a competency-ladder rung -- not a vague trait like "needs more
leadership presence."

</details>

**Q6 (co-06 -- competency-ladders).** What makes a ladder-behavior mapping well-formed?

<details>
<summary>Answer</summary>

It cites the ladder's own stated behavior text verbatim as the standard being checked against, not
a manager's subjective paraphrase of what that behavior means.

</details>

**Q7 (co-07 -- performance-management-and-calibration).** What makes a calibration note comparing
two reports well-formed?

<details>
<summary>Answer</summary>

Every comparative claim cites ladder-level evidence for each person, not a relative popularity
impression like "I like both, X edges out Y."

</details>

**Q8 (co-08 -- delegation-and-context-setting).** What must a delegation brief contain, and what
must it deliberately omit?

<details>
<summary>Answer</summary>

It must contain the what and the why (including the real constraints); it must omit the how. A
reader unfamiliar with the manager's own private reasoning should still be able to reach the same
decision from the brief alone.

</details>

**Q9 (co-09 -- team-delivery-stewardship).** What makes a WIP (work-in-progress) triage well-formed?

<details>
<summary>Answer</summary>

Every blocked item has a named owner -- the manager personally, a delegate, or an escalation
target -- and a one-sentence reason for that specific ownership choice.

</details>

**Q10 (co-10 -- prioritization-under-competing-demands).** What four things must a prioritization
record state?

<details>
<summary>Answer</summary>

The options considered, the trade-off made, the decision, and the communication plan (who gets told
what, and when).

</details>

**Q11 (co-11 -- dora-metrics-as-outcome-lens).** What is the current state of Google's DORA metrics
model, and how should a diagnostic recommendation use it?

<details>
<summary>Answer</summary>

Originally four keys (deployment frequency, lead time, change-failure rate, time-to-restore), now
formalized by Google Cloud's DORA program as a five-metric throughput/instability model. A
recommendation should tie directly to the specific metric that's weak, not a generic "let's move
faster" applied regardless of which number is actually the problem.

</details>

**Q12 (co-12 -- technical-strategy).** What must every bet in a technical strategy trace to?

<details>
<summary>Answer</summary>

A stated product or business outcome, with its trade-off stated explicitly -- not presented as
obviously, uncontroversially correct.

</details>

**Q13 (co-13 -- roadmap-partnership-with-product).** What makes a roadmap-negotiation memo
well-formed?

<details>
<summary>Answer</summary>

It states the specific cost, risk, or dependency being represented, not a vague, unquantified
technical objection like "this is risky."

</details>

**Q14 (co-14 -- communicating-tradeoffs).** What test tells you a trade-off was communicated well?

<details>
<summary>Answer</summary>

A reader who wasn't in the room can state, in their own words, what was gained and what was given
up.

</details>

**Q15 (co-15 -- culture-and-psychological-safety).** What must a well-formed culture diagnosis
name?

<details>
<summary>Answer</summary>

The specific safety failure (why the information didn't surface sooner) and one concrete, recurring
mechanism that would change it -- not a one-time announcement or exhortation.

</details>

**Q16 (co-16 -- hiring-intuition).** What must every score in a hiring evaluation cite?

<details>
<summary>Answer</summary>

Specific observed evidence from the interview loop -- not an unstructured overall impression like
"I really liked them."

</details>

**Q17 (co-17 -- influence-without-authority).** What must an influence-without-authority plan name?

<details>
<summary>Answer</summary>

A shared incentive the other party already holds -- not an appeal to the requester's own authority
or urgency.

</details>

**Q18 (co-18 -- org-design-and-team-topology).** What must a team-topology memo name explicitly?

<details>
<summary>Answer</summary>

Conway's Law, and the predicted resulting system-boundary shift -- not merely the org-chart shift.

</details>

**Q19 (co-19 -- learning-as-a-team-norm).** What must a learning-ritual design name to count as
truly institutionalized?

<details>
<summary>Answer</summary>

The specific mechanism (not just a stated intention) that keeps the ritual running once its
original owner leaves -- for example, a rotation tied to an existing shared calendar.

</details>

**Q20 (co-20 -- manager-vs-maker-tension).** What must a manager-vs-maker diagnosis name?

<details>
<summary>Answer</summary>

The specific bottleneck the manager's own hands-on work created, and one concrete habit change to
correct it.

</details>

## Applied scenarios

Sixteen scenarios. Each is self-contained -- everything you need is in the prompt itself, no other
page required. Decide which concept and which move applies, then check.

**AS1.** A manager says "my door is always open" but never runs a recurring 1:1. A report almost
never brings anything up. What mechanism is likely missing?

<details>
<summary>Answer</summary>

A report-owned recurring channel (co-02). An open-ended, ambiguous invitation puts the entire burden
of initiating on the report; a dedicated, recurring, report-owned 1:1 removes that ambiguity by
existing on the calendar regardless.

</details>

**AS2.** After a strong quarter, a manager tells a report "you're doing great, keep it up!" What's
missing to make this SBI, and why does it matter?

<details>
<summary>Answer</summary>

No situation or specific behavior is named (co-03) -- the report can't tell which exact action to
repeat. "You handled the multi-currency edge case cleanly last sprint" tells the report something
concrete; "you're doing great" doesn't.

</details>

**AS3.** A manager explains the fix to a stuck engineer in full detail every single time. Six
months later, the engineer still asks the same category of question. What went wrong?

<details>
<summary>Answer</summary>

Always directing, never coaching (co-04) -- the engineer never practiced the underlying reasoning,
so nothing about diagnosing this class of problem actually transferred.

</details>

**AS4.** A growth plan says a report "needs to be more strategic." What's the fix?

<details>
<summary>Answer</summary>

Replace the vague trait with an observable behavior cited from the competency ladder's own text
(co-05, co-06) -- for example, "proposes a design approach before coding and defends a trade-off in
it."

</details>

**AS5.** Two managers debate whether an engineer is "ready for senior" with nothing but their own
gut impressions to compare. What's missing?

<details>
<summary>Answer</summary>

A shared competency ladder with quoted behavior text (co-06), cited as evidence in a calibration
note (co-07) -- without it, the debate has no shared standard to resolve against.

</details>

**AS6.** A manager delegates a migration by saying only "handle it however you think is best," with
zero context, then is upset the engineer picked an approach the manager strongly disagrees with.
Whose failure is this?

<details>
<summary>Answer</summary>

The manager's (co-08) -- the brief lacked the what, the why, and the real constraints, so the
engineer had no way to reach a decision compatible with reasoning they were never given.

</details>

**AS7.** Three engineers are each separately blocked on the same undocumented API question all
week, and nobody notices until the sprint ends. What's missing at the team level?

<details>
<summary>Answer</summary>

A stewardship/triage habit (co-09) that surfaces cross-person blockers as they happen, rather than
only discovering the pattern in retrospect.

</details>

**AS8.** A manager quietly decides to postpone a tech-debt project, tells no one, and is later
blindsided by "why did this never happen?" What's missing?

<details>
<summary>Answer</summary>

An explicit, communicated prioritization record (co-10) -- the options, the trade-off, the
decision, and who was told what, written down instead of decided silently.

</details>

**AS9.** A team's deployment frequency is low, but its change-failure rate is 25%. What should the
manager NOT recommend, and why?

<details>
<summary>Answer</summary>

Don't recommend "deploy more often" (co-11) -- a 25% change-failure rate means the team's real
problem is shipping safety, not throughput; pushing frequency without fixing safety would make the
weak metric worse, not better.

</details>

**AS10.** A team ships a steady stream of small, disconnected tools with no unifying direction; six
months later nobody can explain why the system looks the way it does. What's missing?

<details>
<summary>Answer</summary>

A stated technical strategy (co-12) naming a small number of deliberate bets tied to outcomes --
without it, the system's shape is still being decided, just through a hundred unexamined defaults.

</details>

**AS11.** Engineering tells product "that's too risky" with no further detail, and product
overrides the objection and ships anyway. What should engineering have done differently?

<details>
<summary>Answer</summary>

Name the specific cost, risk, or dependency in comparable terms (co-13) -- a vague, unquantified
objection gives product nothing concrete to weigh against their own priorities.

</details>

**AS12.** A manager makes a trade-off decision, never explains it, and a stakeholder later reacts
with surprise or anger when the hidden cost becomes visible on its own. What's missing?

<details>
<summary>Answer</summary>

A legible trade-off communication made upfront (co-14) -- stakeholders who don't understand what a
decision cost tend to assume it cost nothing.

</details>

**AS13.** A retro reveals a real blocker was known a full week before a deadline slipped, but
nobody raised it. What earlier moment usually explains a pattern like this?

<details>
<summary>Answer</summary>

Some earlier moment (often small, often unnoticed by the person who caused it) where raising a
similar concern was met with dismissal (co-15) -- setting an unspoken norm that speaking up again
wouldn't be welcome.

</details>

**AS14.** An interviewer's entire debrief is "I just have a good feeling about this candidate."
What's the risk, and the fix?

<details>
<summary>Answer</summary>

The risk: the evaluation is dominated by whichever interviewer's gut impression is loudest or
speaks last, and by similarity bias (co-16). The fix: a structured scorecard where every score cites
specific observed evidence from the loop.

</details>

**AS15.** A manager asks a peer team to "prioritize this because I'm asking nicely" and gets
politely ignored. What's missing?

<details>
<summary>Answer</summary>

A named shared incentive (co-17) -- the peer team has no reporting obligation and no stated reason
of their own to prioritize the ask; naming what they already gain from it would give them one.

</details>

**AS16.** A reorg redraws team boundaries purely by headcount balance, with no attention to the
software those teams currently touch. Six months later, a confusing new coupling appears that
nobody predicted. What step was skipped?

<details>
<summary>Answer</summary>

A Conway's Law prediction (co-18) made before committing to the reorg -- naming, in advance, which
system boundary the new team-communication structure would harden, so the coupling would have been
a deliberate, accepted choice instead of a surprise.

</details>

## Artifact recreation drills

Eight before/after decision-artifact repair drills. Each gives a flawed, self-contained mocked
artifact -- spot and fix the flaw yourself, then compare against the "after" version and its
root-cause explanation.

### Drill 1 -- a 1:1 agenda that's actually a status update

**Before**: "Weekly 1:1 agenda: 1. Sprint status update from me. 2. Any blockers I should know
about. 3. Anything else."

<details>
<summary>Model fix and root cause</summary>

**After**: "1. Anything blocking you right now? 2. Anything on your mind about the work or your own
growth? 3. Anything you want feedback on? [Manager's items, added only after the above is covered]: 4. One thing I want to flag this week."

**Root cause**: co-02 requires the report's items to lead the agenda; the "before" version starts
with the manager's own status check, quietly training the report that this meeting belongs to the
manager, not to them.

</details>

### Drill 2 -- feedback that's vague praise

**Before**: "Nice work this sprint, really appreciate the effort!"

<details>
<summary>Model fix and root cause</summary>

**After**: "Situation: Tuesday's currency-service deploy. Behavior: you paused the rollout and
traced a rounding discrepancy before it shipped. Impact: that prevented a customer-facing invoice
bug."

**Root cause**: co-03 requires a specific situation, behavior, and impact. "Nice work" gives the
report nothing to consciously repeat next time something similar comes up.

</details>

### Drill 3 -- a growth-plan gap stated as a vague trait

**Before**: "Gap: needs to show more ownership."

<details>
<summary>Model fix and root cause</summary>

**After**: "Gap: doesn't yet propose the technical approach before starting work -- waits to be
told the design. Next-level behavior (per the ladder): 'proposes a design approach for a multi-day
task before writing code, and can defend a trade-off in it.'"

**Root cause**: co-05 and co-06 require every gap to map to an observable, ladder-quoted behavior.
"Show more ownership" gives the report nothing concrete to start doing differently.

</details>

### Drill 4 -- a delegation brief that specifies the how

**Before**: "Add an in-process cache with a 5-minute TTL to the lookup table -- go ahead and build
it that way."

<details>
<summary>Model fix and root cause</summary>

**After**: state the what (stop the round trip), the why (the latency budget and where it's being
spent), and the real constraints (staleness tolerance, no new infra dependency) -- leave the
specific caching mechanism for the engineer to choose.

**Root cause**: co-08 requires the how to stay deliberately unspecified. The "before" version
dictates the exact mechanism, which defeats the point of delegating the decision at all.

</details>

### Drill 5 -- a prioritization record with no communication plan

**Before**: "Decision: we're doing the ETL rewrite first, feature work is delayed."

<details>
<summary>Model fix and root cause</summary>

**After**: add the options considered, the specific trade-off made, and a stated communication
plan -- who (product, the team) gets told what, and when.

**Root cause**: co-10 requires all four elements. A bare decision with no stated options or
communication plan gets re-litigated the first time someone asks why, because nothing explains the
reasoning or who was supposed to already know.

</details>

### Drill 6 -- a DORA recommendation that's generic "go faster"

**Before**: "Our DORA numbers need work -- let's all try to move faster this quarter."

<details>
<summary>Model fix and root cause</summary>

**After**: identify which specific metric is weak (for example, lead time, driven by a 4-day PR
review turnaround) and recommend a fix targeted at that specific bottleneck (a same-day review SLA).

**Root cause**: co-11 requires the recommendation to tie to the specific weak metric. A blanket
"move faster" risks re-optimizing metrics that were already healthy while leaving the real
bottleneck untouched.

</details>

### Drill 7 -- a hiring debrief that's an unstructured gut call

**Before**: "Great candidate, I really liked them, let's hire."

<details>
<summary>Model fix and root cause</summary>

**After**: score each role-specific signal separately, citing specific observed evidence from the
loop for each -- for example, "systems-design judgment: 4, caught a hot-partition risk unprompted
in the design round."

**Root cause**: co-16 requires every score to cite specific observed evidence. An unstructured "I
really liked them" is dominated by whichever interviewer speaks first or most confidently in the
debrief.

</details>

### Drill 8 -- a reorg memo that doesn't name Conway's Law

**Before**: "We're splitting the team into Ingestion and Serving to balance headcount better."

<details>
<summary>Model fix and root cause</summary>

**After**: name Conway's Law explicitly and state the predicted system-boundary shift -- for
example, the currently informal internal event format will harden into a versioned, contract-tested
API within two quarters, because two separate teams can no longer coordinate an informal change
with a same-day message.

**Root cause**: co-18 requires the memo to name Conway's Law and predict the resulting system
boundary. A headcount-only justification misses the technical consequence the reorg will actually
have.

</details>

## Self-check checklist

Confirm each item without checking the concepts page first. If you hesitate, that concept needs
another pass.

- [ ] I can name the core change from IC to manager and explain why the old reflex is hard to
      unlearn. (co-01)
- [ ] I can design a 1:1 agenda that puts the report's items ahead of the manager's. (co-02)
- [ ] I can write feedback -- both reinforcing and corrective -- that names a specific situation,
      behavior, and impact. (co-03)
- [ ] I can write a coaching response that supplies only questions, no answer. (co-04)
- [ ] I can write a growth plan where every gap maps to an observable, ladder-quoted behavior.
      (co-05)
- [ ] I can map a report's recent actions onto specific competency-ladder rungs, citing the
      ladder's own text. (co-06)
- [ ] I can write a calibration note that compares two reports using ladder-level evidence, not
      a popularity impression. (co-07)
- [ ] I can write a delegation brief that states the what and why while leaving the how
      unspecified. (co-08)
- [ ] I can triage a week's blockers into personally-unblock, delegate, or escalate, with a
      reason for each. (co-09)
- [ ] I can write a prioritization record stating options, trade-off, decision, and communication
      plan. (co-10)
- [ ] I can read a team's DORA metrics and tie a recommendation to the specific weak one, not a
      generic push. (co-11)
- [ ] I can write a technical strategy where every bet traces to a product outcome with an
      explicit trade-off. (co-12)
- [ ] I can write a roadmap-negotiation memo that states a specific cost, risk, or dependency, not
      a vague objection. (co-13)
- [ ] I can communicate a trade-off so a reader who wasn't in the room can restate what was gained
      and given up. (co-14)
- [ ] I can diagnose a psychological-safety failure and design a recurring mechanism, not a
      one-time fix. (co-15)
- [ ] I can score a hiring candidate against role-specific signals, citing observed evidence for
      each. (co-16)
- [ ] I can write an influence-without-authority plan that names a shared incentive, not an appeal
      to authority. (co-17)
- [ ] I can predict, using Conway's Law, how a team-topology change will reshape a system
      boundary. (co-18)
- [ ] I can design a learning ritual with a mechanism that survives its original owner leaving.
      (co-19)
- [ ] I can diagnose a manager-vs-maker slip, naming the bottleneck it created and a corrective
      habit. (co-20)
- [ ] I can explain, in one sentence, why leadership is disciplined compromise, not a search for
      the ideal answer. (`correctness-vs-pragmatism`)
- [ ] I can explain, in one sentence, why a manager sets policy and delegates mechanism instead of
      owning every "how" personally. (`mechanism-vs-policy`)

## Elaborative interrogation and self-explanation

Six why/why-not prompts, tied to this topic's two cross-cutting big-idea tags. Answer each in your
own words before opening the model explanation.

**E1 (`correctness-vs-pragmatism`).** Why is a prioritization decision that leaves a real,
legitimate demand unaddressed often the _correct_ call, rather than a leadership failure?

<details>
<summary>Model explanation</summary>

A team's capacity is always finite, and every competing demand (Worked Scenario 10's dashboard
feature, ETL rewrite, and on-call load are all genuinely real) can't be fully addressed
simultaneously. Leadership here means making the trade-off explicit and chosen -- naming exactly
what's being deferred and why -- rather than pretending all three can be done at once. Calling
that a "failure" mistakes the existence of a trade-off for evidence of a bad decision; the actual
failure would be making the same trade-off silently, with no stated reasoning.

</details>

**E2 (`correctness-vs-pragmatism`).** Why does a decision made under real uncertainty (an
estimate, a delegation call, a hiring score) count as rigorous, rather than as cutting corners?

<details>
<summary>Model explanation</summary>

Waiting for certainty before deciding isn't more rigorous -- it's a different, often more expensive
way of avoiding the decision. Rigor here means anchoring the judgment to the best available
evidence (a ladder's stated behavior text, an interview loop's specific observed evidence, a DORA
metric's actual weak point) and stating it explicitly, not achieving certainty that leadership
decisions never actually have available. The discipline is honest, evidence-anchored judgment under
uncertainty, not false confidence dressed up as certainty.

</details>

**E3 (`correctness-vs-pragmatism`).** Why is the manager-vs-maker tension something to be actively
managed on a recurring basis, rather than a problem a manager solves once and moves past?

<details>
<summary>Model explanation</summary>

The pull toward hands-on work never fully disappears, because it's the exact reflex that made the
manager a strong engineer in the first place, and every high-pressure incident re-creates the
temptation to just fix it personally rather than coach through it. Treating it as "solved" after one
good habit-change memo (Worked Scenario 8) ignores that the next Thursday-morning incident applies
the same pressure again -- the discipline is catching the slip each time it recurs (Worked Scenario
9), not assuming one memo makes the reflex permanently go away.

</details>

**E4 (`mechanism-vs-policy`).** Why does a manager delegate the "how" while retaining the "what and
why," rather than either fully directing every detail or stepping back from the decision entirely?

<details>
<summary>Model explanation</summary>

Fully directing the how wastes the report's own judgment and keeps the manager as the bottleneck on
every decision of that class; stepping back with no context at all leaves the report unable to make
a decision compatible with reasoning they were never given, and produces either paralysis or a
confidently wrong call. Retaining the what and why while delegating the how is the specific split
that lets someone else make the same call the manager would -- policy (the goal, the constraints
that matter) stays set centrally; mechanism (the specific implementation) is where local judgment
adds the most value.

</details>

**E5 (`mechanism-vs-policy`).** How does Conway's Law illustrate a policy decision (org design)
determining a mechanism outcome (system structure), and why does that make org design an
engineering lever, not just an HR exercise?

<details>
<summary>Model explanation</summary>

A reorg is, on its surface, a policy-level decision about who reports to whom and how teams are
grouped. Conway's Law states that this policy choice mechanically determines how the system itself
ends up structured, because a system's architecture tends to mirror the communication structure of
the organization that built it (Worked Scenario 21's predicted Ingestion/Serving boundary
hardening). Treating org design as purely a headcount or reporting-line exercise ignores that it is
simultaneously making a technical architecture decision, whether or not anyone intended it to.

</details>

**E6 (`mechanism-vs-policy`).** Why does influence without authority rely on naming a shared
incentive (a policy-level alignment) rather than directing someone's actions (a mechanism-level
lever a manager doesn't actually have over a peer)?

<details>
<summary>Model explanation</summary>

A manager has no mechanism-level control over a peer team -- no reporting line, no ability to
assign their work. The only lever available is policy-level: showing the peer team that their own
already-existing goals (Worked Scenario 18's Data Science team already wants fewer pages) align with
the requested change. Naming the shared incentive works because it doesn't require any authority at
all -- it simply makes visible an alignment that was already there, which is the only kind of
influence available when mechanism-level control is absent by design.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md) · Next: [34 · NoSQL
Databases](../../nosql-databases/learning/overview.md) →
