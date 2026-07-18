---
title: "Intermediate Scenarios"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 20
---

Scenarios 10-19 move from single-report conversations to team-level stewardship: prioritizing
competing demands, reading DORA metrics as a diagnostic, triaging blockers across people,
calibrating performance across two reports, scripting a hard feedback conversation about a pattern,
representing engineering in a roadmap negotiation, diagnosing a psychological-safety failure,
running a structured hiring debrief, planning influence without authority, and making a culture-norm
change stick. Most scenarios continue following **Everline**'s Platform team, led by **Priya
Kapoor** -- every name, number, and quote below is an illustrative, constructed example, not a real
transcript. Every artifact below also lives, standalone, under `learning/artifacts/`.

---

### Worked Scenario 10: Prioritization Decision Record

**Context**: Exercises co-10, co-14. The Platform team faces three competing demands for Q2: a
product-requested real-time dashboard-alerts feature, a fragile ETL script that keeps causing
data-quality incidents, and rising on-call pager load. Priya writes the team's prioritization
decision record.

**Decision artifact**:

> **Options considered**: (1) ship the dashboard-alerts feature first, delaying the ETL rewrite and
> on-call work; (2) rewrite the fragile ETL script first, delaying the feature by a full quarter;
> (3) split effort three ways, delivering all three slowly.
>
> **Trade-off**: option 3 was ruled out first -- splitting a 7-person team three ways on
> already-tight capacity means none of the three lands well, and the ETL script's failure mode
> (silent data-quality incidents) actively gets worse the longer it's deferred. Between options 1
> and 2, the team chose a modified option 2: rewrite the highest-risk third of the ETL script this
> quarter (the part causing 80% of the incidents), and ship a scoped-down version of the
> dashboard-alerts feature in parallel with the remaining capacity, deferring the full feature scope
> to Q3.
>
> **Decision**: partial ETL rewrite (highest-risk portion) plus a scoped dashboard-alerts MVP, this
> quarter. On-call load reduction is explicitly deferred to next quarter's prioritization pass.
>
> **Communication plan**: Priya tells product directly (not via a status doc) that the
> dashboard-alerts feature ships scoped-down this quarter, full scope Q3, and why (data-quality risk
> won out over full feature scope); she tells the team in the next planning meeting, with the
> incident-rate reasoning attached so the decision doesn't read as arbitrary.

**Verify**: the record states the options considered (three, including the rejected split-effort
option), the trade-off made (highest-risk ETL portion over on-call work, over full feature scope),
the decision (partial rewrite plus scoped feature), and the communication plan (who gets told what,
and how) -- satisfying co-10 and co-14's rule.

**Key takeaway**: The record doesn't pretend all three demands got fully addressed -- it names
exactly what got traded away (on-call load reduction, full feature scope) and why, so nobody has to
guess later why the on-call situation didn't improve this quarter.

**Why It Matters**: An undocumented version of this same decision gets re-litigated every time
someone on product asks "why isn't the full feature done yet" -- the written record turns a one-time
argument into a decision the team can point back to and revisit deliberately, not relitigate from
scratch.

---

### Worked Scenario 11: DORA Diagnostic Memo

**Context**: Exercises co-11. Priya reads the Platform team's quarterly DORA numbers and writes a
diagnostic memo naming where to invest next.

**Decision artifact**:

> **This quarter's numbers**: deployment frequency -- 3 deploys/week (healthy for this team's
> size); change-failure rate -- 8% (healthy, below the team's own 10% target); failed-deployment
> recovery time -- 40 minutes (healthy); lead time for changes -- 6 days from first commit to
> production (the outlier -- every other metric is solid).
>
> **Diagnosis**: the team isn't shipping recklessly (change-failure rate is fine) and isn't slow to
> recover when something does break (recovery time is fine) -- the bottleneck is specifically how
> long a change sits before it ships at all. Looking at where the 6 days actually goes: roughly 4 of
> them are PR review turnaround, not implementation time.
>
> **Recommendation**: invest in review turnaround specifically -- a same-day review SLA and
> designating two rotating "review-first" engineers per week -- not a generic "let's move faster"
> push on implementation speed, which isn't where the time is actually going.

**Verify**: the recommendation ties directly to the specific weak metric (lead time, and the review
turnaround within it), not a generic "go faster" applied to the whole team regardless of which
number is the actual problem -- satisfying co-11's rule.

**Key takeaway**: Three of the four numbers were already healthy -- a blanket "let's improve our
DORA metrics" initiative would have wasted effort re-optimizing things that weren't broken. The
diagnosis only works because it isolates which specific number is weak before proposing a fix.

**Why It Matters**: A manager who reads "our DORA numbers need work" as one undifferentiated signal
risks fixing the wrong thing -- a team with Priya's exact healthy-except-lead-time profile needs a
completely different intervention than a team with a high change-failure rate, and treating them the
same wastes the team's limited improvement capacity.

---

### Worked Scenario 12: WIP Unblock Triage

**Context**: Exercises co-09. Five items are blocked across the Platform team this week. Priya
triages each into what she personally unblocks, delegates, or escalates.

**Decision artifact**:

> | Blocked item                                                                                    | Owner                       | Reason                                                                                                                            |
> | ----------------------------------------------------------------------------------------------- | --------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
> | Sam's migration script blocked on a schema question only Priya can answer (pre-dates the team). | Priya, personally           | Only Priya has the historical context; this is a 10-minute answer, not worth delegating.                                          |
> | Alex's ingestion service blocked on a security review with no ETA from the Security team.       | Priya, escalate             | Outside the team's control; needs manager-to-manager escalation to get a review date.                                             |
> | Maya's design note blocked on Jordan's availability to pair-review it.                          | Delegate to Jordan directly | A scheduling problem between two ICs; Priya doesn't need to be in the loop, just needs to confirm it's moving.                    |
> | Chris's dashboard work blocked on an ambiguous product spec.                                    | Delegate to Chris           | Chris can resolve this directly with the product manager; Priya adding herself would slow it down, not speed it up.               |
> | Dana's staging environment blocked on a flaky test suite nobody owns.                           | Priya, personally           | No current owner and it's been blocking three people intermittently for two weeks -- worth Priya taking it to force a resolution. |

**Verify**: every blocked item has a named owner (Priya personally, a named delegate, or an
escalation target) and a one-sentence reason for that specific ownership choice -- satisfying
co-09's rule.

**Key takeaway**: Priya doesn't default to "I'll handle it" for every blocker -- she personally
takes only the two items that genuinely need her (unique context, or a stalled owner-less problem),
and explicitly routes the other three to the people actually positioned to resolve them fastest.

**Why It Matters**: A manager who unblocks everything personally becomes the team's single point of
failure for getting unstuck at all -- the triage table makes visible, item by item, which blockers
actually require the manager and which ones the manager was just defaulting to owning out of habit.

---

### Worked Scenario 13: Performance Calibration Note

**Context**: Exercises co-07, co-06. Priya compares Chris's and Dana's recent impact against the
same Senior Engineer ladder rung ahead of a calibration conversation with her own manager.

**Decision artifact**:

> **Chris vs Dana -- Senior Engineer rung: "proposes a design approach before coding, and can
> defend a trade-off in it."**
>
> **Chris**: proposed and defended two design notes this quarter (the retry-queue rework and the
> alert-batching change), both reviewed and adopted with only minor changes. Meets the rung
> consistently, not as a one-off.
>
> **Dana**: proposed one design note this quarter (the schema-versioning approach), which needed a
> full second pass after review surfaced a missed edge case Dana hadn't considered. Partially meets
> the rung -- the initiative is there, the defensibility under review is not yet consistent.
>
> **Calibration note**: Chris is closer to ready for the Senior Engineer conversation on this
> specific rung than Dana is, based on two independently reviewed design notes versus one that
> needed rework -- not because Chris is "more senior overall" in some general sense.

**Verify**: the comparative claim cites ladder-level evidence for both people (two adopted design
notes for Chris; one design note needing rework for Dana), not a relative popularity impression like
"I like both, Chris edges out Dana" -- satisfying co-06 and co-07's rule.

**Key takeaway**: The note is careful to compare on one specific rung, not overall likability or
tenure -- Dana might be ahead of Chris on a different rung entirely; this calibration only settles
the one dimension it actually examined.

**Why It Matters**: Calibration conversations that run on gut feel ("Chris just seems more senior")
are indefensible the moment someone asks why, and they erode trust in the whole promotion process --
citing the same ladder text for both people is what makes the comparison something Priya could
defend to Chris, to Dana, or to her own manager, using the same evidence each time.

---

### Worked Scenario 14: Difficult Feedback Conversation Script

**Context**: Exercises co-03, co-07. Sam has now missed three committed deadlines over two months
(the schema-migration script from Worked Scenario 3, plus two more since). Priya scripts a
conversation about the pattern, not just the latest miss.

**Decision artifact**:

> **Opening (names the pattern, not the latest miss)**: "I want to talk about something I'm seeing
> across the last two months, not just this week. Three times now -- the migration script in April,
> the alert-batching work in May, and this week's dashboard task -- you've missed a committed date
> without flagging it in advance. I want to understand what's going on, because it's a pattern now,
> not a one-off."
>
> **Space for Sam's side**: "Before I say more -- what's your read on what's happening across these
> three? Is it estimation, is it something getting in the way partway through, is it something
> else?"
>
> **Naming the impact plainly**: "Whatever the cause, the effect on my side is that I can't commit
> dates to product with confidence when your work is on the critical path, and that's starting to
> cost the team's credibility, not just this task's timeline."
>
> **One named next step**: "For the next four weeks, let's do a mid-task check-in every Wednesday --
> just a two-line async update on whether you're still on track -- so if something's slipping, I
> hear about it Wednesday, not the day it's due."

**Verify**: the script opens with the pattern (three dated instances across two months), not the
latest single miss, and ends with exactly one named next step (a weekly Wednesday check-in) --
satisfying co-03 and co-07's rule.

**Key takeaway**: The script deliberately asks Sam's read before Priya offers her own theory --
naming the pattern doesn't mean assuming the cause; a check-in cadence works whether the real
problem turns out to be estimation, an unstated blocker, or something else entirely.

**Why It Matters**: Addressing only the latest miss ("hey, the dashboard task was late") would let
Sam reasonably read it as a one-off correction, missing that this is Priya's third time raising
essentially the same issue -- naming the pattern explicitly is what turns three isolated
conversations into one conversation Sam can actually act on.

---

### Worked Scenario 15: Roadmap Trade-off Memo

**Context**: Exercises co-13, co-14. Product wants multi-currency support shipped by end of quarter;
Priya represents the engineering cost and risk of doing that before a required schema migration is
done.

**Decision artifact**:

> **The trade-off being asked of product**: multi-currency support touches the same event-schema
> tables the team is mid-migration on. Building it before the migration finishes means either (a)
> building it twice -- once against the old schema, once against the new -- or (b) accepting real
> data-integrity risk during the transition window while both schemas coexist.
>
> **What we're proposing instead**: finish the schema migration first (3 weeks, already in flight)
> and start multi-currency support immediately after, landing 2 weeks later than product's original
> ask but built once, against the final schema, with no transition-window risk.
>
> **What product is being asked to accept**: a 2-week slip against the original target date, in
> exchange for not paying for the feature twice and not carrying data-integrity risk into the
> release.

**Verify**: the memo states the specific trade-off product is being asked to accept (a 2-week slip,
in exchange for avoiding double-build cost and integrity risk), not a vague technical objection like
"this is risky" -- satisfying co-13 and co-14's rule.

**Key takeaway**: Priya doesn't just say no to the original date -- she names the actual cost of
saying yes (build twice, or accept integrity risk) and proposes a specific alternative with its own
stated cost (2 weeks), so product is negotiating with real numbers instead of an open-ended
technical veto.

**Why It Matters**: An engineering team that only ever says "that's risky" without quantifying the
risk regularly loses roadmap negotiations to a product team that can point to a concrete date --
naming the actual trade-off in comparable terms (2 weeks vs. double-build cost) is what makes the
technical concern something product can genuinely weigh, not override by default.

---

### Worked Scenario 16: Psychological Safety Incident

**Context**: Exercises co-15. The dashboard-alerts feature slipped its deadline; in the retro, it
comes out that Chris knew the staging environment's flakiness was going to cause the delay a full
week before the deadline, but didn't say anything until after it slipped. Priya diagnoses why.

**Decision artifact**:

> **The safety failure**: in a planning meeting two weeks earlier, someone raised a staging-flakiness
> concern and Priya (rushed, focused on the sprint commitment) responded "let's not use that as an
> excuse, we've committed to this date." Chris was in that meeting. When staging got worse the
> following week, Chris read the earlier response as "raising this again won't be welcome" and
> stayed quiet rather than risk a repeat of that reaction.
>
> **Concrete norm change**: starting next retro, Priya adds a standing agenda item -- "what did
> someone almost say this sprint but didn't?" -- asked explicitly, every retro, whether or not
> anything obviously went wrong. This isn't a one-time apology or a single "please speak up" email;
> it's a recurring prompt built into the ritual that already happens every two weeks, so the
> invitation to raise a concern doesn't depend on anyone remembering it was offered once.

**Verify**: the diagnosis names the specific safety failure (Priya's own rushed dismissal, and how
Chris read it) and one concrete, recurring mechanism to fix it (a standing retro agenda item, not a
one-time announcement) -- satisfying co-15's rule.

**Key takeaway**: The fix isn't "be nicer next time a concern comes up" -- it's a specific,
repeating structural change to the retro ritual itself, because the failure wasn't really about
niceness; it was about one offhand dismissal quietly setting a norm that outlasted the moment it
happened in.

**Why It Matters**: The information that would have prevented the slip existed a full week before
the deadline -- the cost of this incident wasn't a lack of technical skill anywhere on the team, it
was entirely the cost of one moment where speaking up felt unsafe, which is exactly what
psychological safety is meant to prevent.

---

### Worked Scenario 17: Hiring Debrief, Structured

**Context**: Exercises co-16. Taylor, a candidate for a Platform team opening, just finished the
interview loop. Priya writes a structured debrief scoring Taylor against role-specific signals.

**Decision artifact**:

> | Signal                           | Evidence from the loop                                                                                                                                                                                            | Score (1-4)                                |
> | -------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ |
> | Systems-design judgment          | In the design round, Taylor correctly identified that the proposed schema would create a hot partition under the stated load, and proposed two concrete alternatives with trade-offs, unprompted.                 | 4 -- strong, unprompted evidence           |
> | Debugging rigor                  | In the debugging exercise, Taylor formed and tested three hypotheses in order of likelihood before finding the root cause, narrating the reasoning throughout.                                                    | 4 -- strong, unprompted evidence           |
> | Collaboration under disagreement | When the interviewer pushed back on Taylor's first design choice, Taylor asked a clarifying question, then revised the proposal rather than defending the original -- but this only showed up once, in one round. | 3 -- solid, but only one observed instance |
>
> **Overall recommendation**: hire -- two of three signals show strong, unprompted evidence across
> multiple rounds; the third shows one clean instance but wasn't tested more than once.

**Verify**: every score cites specific observed evidence from the interview loop (the hot-partition
catch, the ordered-hypothesis debugging, the one revision-after-pushback moment), not an
unstructured overall impression like "I really liked them" -- satisfying co-16's rule.

**Key takeaway**: The debrief doesn't average out to a single gut number -- it keeps the three
signals separate, which matters here because the collaboration signal is genuinely thinner evidence
than the other two, and a future interview loop for this candidate (or the next one) should probably
test it more than once.

**Why It Matters**: An unstructured "great candidate, hire them" debrief is dominated by whichever
interviewer speaks first or most confidently in the debrief meeting -- a structured, evidence-cited
scorecard resists that, and it gives the next interviewer on the loop something concrete to test
further if a signal's evidence is thin.

---

### Worked Scenario 18: Influence-Without-Authority Plan

**Context**: Exercises co-17. Priya wants Morgan, who leads Everline's separate Data Science team,
to adopt a shared schema-registry contract for the events both teams depend on. Morgan doesn't
report to Priya, and vice versa.

**Decision artifact**:

> **What Priya wants**: Data Science adopts the same schema-registry contract-testing tooling
> Platform already uses, so schema changes on either side get caught before they break the other
> team's pipeline.
>
> **The shared incentive named**: Data Science was paged twice last month for pipeline failures
> caused by an undocumented schema change Platform made -- Morgan's team is already paying the cost
> of the exact problem this proposal fixes; this isn't a favor being asked of Morgan, it's a shared
> problem with a shared fix.
>
> **The ask, framed around that incentive**: "Your team got paged twice last month because of an
> undocumented schema change on our side. If both teams adopt the same contract-testing check, that
> stops happening to either of us -- I'll pair with whoever on your team owns this to get it set up
> against your existing pipeline first, so it costs your team close to nothing to adopt."

**Verify**: the plan names a shared incentive Morgan's team already holds (being paged for exactly
this class of failure) rather than appealing to Priya's own authority or urgency ("I need this," "my
team needs this by Friday") -- satisfying co-17's rule.

**Key takeaway**: The pitch doesn't ask Morgan to do Priya a favor -- it names a cost Morgan's team
is already paying and offers to absorb the setup effort, which is a fundamentally different, much
easier ask than "please prioritize my request."

**Why It Matters**: "Can you prioritize this for me" gives a peer with no reporting obligation no
actual reason to say yes over their own team's priorities -- naming the incentive they already share
(getting paged less) gives Morgan a reason to want this regardless of who's asking.

---

### Worked Scenario 19: Team Culture Norm Change

**Context**: Exercises co-15. Priya proposes moving the Platform team to blameless postmortems after
a small incident got quietly under-investigated because the engineer involved seemed defensive about
it. She designs the mechanism that makes it stick.

**Decision artifact**:

> **The norm**: every production incident above a stated severity gets a written postmortem that
> names contributing factors and system gaps, never an individual's mistake as the root cause.
>
> **The mechanism that makes it stick (not just a one-time announcement)**: postmortem-facilitator
> duty rotates weekly across the team, tracked on the same shared calendar the on-call rotation
> already uses. Whoever is on facilitator duty that week runs the postmortem for any incident that
> happens during it -- not the engineer who was involved, and not always Priya. The rotation makes
> "who runs this" a standing team responsibility, not a thing that depends on Priya remembering to
> announce it or personally showing up every time.

**Verify**: the mechanism (a weekly rotating facilitator duty on a shared calendar) is a recurring
structural feature, not a one-time announcement or a single email declaring the new norm --
satisfying co-15's rule that the mechanism must outlast the announcement.

**Key takeaway**: A single "we're doing blameless postmortems now" announcement would fade the first
time Priya was out sick during an incident -- tying the responsibility to an existing rotation
mechanism (the same one on-call already uses) means the norm keeps running with or without Priya
personally present.

**Why It Matters**: Culture norms that depend on one person's ongoing personal enforcement
disappear the moment that person is unavailable or leaves -- a norm tied to a standing mechanism
(a rotation, a recurring agenda item) survives exactly the kind of absence that would otherwise
quietly kill it.

---

← Previous: [Beginner Scenarios](./beginner.md) · Next: [Advanced Scenarios](./advanced.md) →
