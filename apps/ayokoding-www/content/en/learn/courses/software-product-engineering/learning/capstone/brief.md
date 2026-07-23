---
title: "Product Brief: Auto-Reminder SMS for Upcoming Shifts"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 2
---

> Kestrel -- auto-reminder SMS for upcoming shifts. A compact product brief a team could act on
> directly. Kestrel and every number, quote, and interview finding below are illustrative,
> constructed examples written to teach this topic's techniques -- not a real company, real usage
> data, or a real transcript.

## 1. Problem statement

Employees on a Kestrel-scheduled team currently have no way to be reminded of an upcoming shift
other than actively checking the schedule themselves. For a shift published several days out, in
the middle of a busy week, this is easy to lose track of -- and a forgotten shift produces the same
operational damage as a shift someone consciously blew off: an uncovered position, a scramble to
find last-minute coverage, and a manager's trust in the schedule eroded. We want the rate of
shifts missed specifically because the employee forgot -- as distinct from shifts missed due to a
genuine availability conflict -- brought down. This statement does not yet commit to SMS, email,
push notifications, or any other specific reminder mechanism; which channel (if any) is worth
building is addressed in Section 4.

## 2. Job story and evidence

> When I have a shift three days out that's easy to forget in a busy week, I want a well-timed
> nudge before it happens, so I show up on time without having to actively remember to check the
> schedule myself.

**Evidence**: this problem traces directly to Worked Scenario 19's opportunity-solution tree, where
"employees forget upcoming shifts" was named as the first of three opportunities under the "reduce
no-show shift incidents by 30%" outcome. In that same illustrative dataset, roughly 40% of no-show
incidents tagged that quarter were tagged "forgot," as distinct from "conflict" (the employee
became unavailable after the shift was published) or "no longer employed" -- making "forgot" the
single largest named cause and the one this brief's MVP targets.

## 3. MVP scope and non-goals

**MVP scope**: send an automated SMS reminder to the assigned employee 24 hours before a shift, and
a second SMS reminder 2 hours before the shift. Both reminders are sent automatically once a
schedule is published; no manager action is required per shift.

**Explicit non-goals** (deliberately out of scope for this MVP):

- No per-shift or per-employee customization of reminder timing -- the 24h/2h cadence is fixed for
  every shift in this MVP.
- No reminders for shifts published more than 7 days in advance -- a reminder sent 10 days early
  provides little value and adds unnecessary message volume.
- No email channel -- SMS only for this MVP; email is a possible later addition, not part of this
  scope.
- No per-shift opt-out granularity -- an employee can disable reminders globally in their profile
  settings, but cannot selectively silence reminders for one specific shift while keeping others
  active.

## 4. RICE-ranked backlog

Reference units: Reach in employees receiving at least one reminder per quarter; Impact on
Intercom's discrete scale (3 massive, 2 high, 1 medium, 0.5 low, 0.25 minimal); Confidence as a
percentage; Effort in person-months.

| Backlog item                    | Reach | Impact | Confidence | Effort | RICE                          |
| ------------------------------- | ----- | ------ | ---------- | ------ | ----------------------------- |
| 24-hour-before SMS reminder     | 2000  | 2      | 0.8        | 1.5    | (2000×2×0.8)÷1.5 = **2133.3** |
| 2-hour-before SMS reminder      | 2000  | 1      | 0.7        | 1      | (2000×1×0.7)÷1 = **1400**     |
| In-app reminder banner (no SMS) | 1500  | 0.5    | 0.9        | 0.5    | (1500×0.5×0.9)÷0.5 = **1350** |

**Ranked order**: 24-hour SMS reminder (2133.3) > 2-hour SMS reminder (1400) > in-app reminder
banner (1350).

**Defended ordering**: the 24-hour reminder ranks first because it is the highest-impact, highest-
confidence item -- it targets the specific "forgot entirely, days in advance" failure mode named in
Section 2's evidence, at a cost proportional to its reach. The 2-hour reminder ranks second: it
targets a narrower failure mode (remembered the shift existed but lost track of it on the day
itself) with lower estimated impact and confidence, since Kestrel has no prior data on same-day
reminder effectiveness. The in-app banner ranks third and lowest: it only reaches employees
already actively in the app (smaller effective reach among people who need a reminder in the first
place, since the point of a reminder is reaching people who _aren't_ already looking), giving it
both a lower estimated impact and a narrower true audience than either SMS item, despite its low
cost.

## 5. Metrics: north-star and AARRR mapping

**North-star metric** (unchanged from this topic's earlier north-star work): number of teams with
a published schedule active in the last 7 days -- this feature does not change the north-star
itself, but is expected to support it indirectly.

**Supporting metric for this feature**: no-show rate -- the % of published shifts with no clock-in
recorded and no approved swap on file. This is the feature's direct target metric, distinct from
the north-star, and maps to the **Retention** stage of the AARRR funnel (Worked Scenario 9): a
team whose employees reliably show up for their shifts is a team with fewer operational fires, and
fewer operational fires is a team more likely to keep renewing its Kestrel subscription.

## 6. A/B experiment design

**Hypothesis**: sending an SMS reminder 24 hours and 2 hours before a shift reduces the no-show
rate for shifts tagged "forgot," without meaningfully increasing the rate at which employees opt
out of Kestrel's SMS notifications generally.

**Primary metric (OEC)**: no-show rate on shifts eligible for the reminder (published more than 24
hours in advance).

**Guardrail**: the SMS notification opt-out rate must not increase by more than 1 percentage point
during the experiment window -- a proxy for notification fatigue. A reminder feature that reduces
no-shows while also driving enough employees to disable all Kestrel SMS (including shift-swap
notifications, Worked Scenarios 28-30) would be trading one problem for a different, possibly worse
one.

## 7. Internal consistency

- **Scope serves the problem**: the MVP (Section 3) is scoped specifically around the "forgot"
  failure mode named in Section 1 and Section 2's evidence -- fixed-timing SMS reminders, nothing
  broader. The non-goals explicitly exclude scope creep (per-shift customization, additional
  channels) that would not change whether an employee remembers a shift they'd otherwise forget.
- **Backlog reflects the problem's evidence**: the highest-RICE item (the 24-hour reminder) is the
  one most directly aimed at the "days in advance" pattern in the "forgot" evidence from Section 2,
  not merely the cheapest item to build.
- **Metrics measure the outcome**: the supporting metric (no-show rate) is the direct, measurable
  version of Section 1's stated outcome ("fewer shifts missed because the employee forgot"), not a
  proxy metric several steps removed from it.
- **Experiment tests the hypothesis**: the primary metric (no-show rate on eligible shifts) is
  exactly what Section 1's problem and Section 6's hypothesis both target, and the guardrail
  (SMS opt-out rate) guards against the specific, plausible harm this particular mechanism (SMS
  reminders) could cause that the primary metric alone would not reveal.

This brief is executable without hand-waving: a reader could hand it to a real product trio, and
the team would know exactly what to build, in what order, and how to know whether it worked.
