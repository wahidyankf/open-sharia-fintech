---
title: "Beginner Scenarios"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 10
---

Scenarios 1-8 establish the single-document discipline every later scenario in this topic builds on:
leading with the decision, ordering by importance, passing the skim test, writing a PR reviewers can
act on, cutting hedges, using precise requirement keywords, matching an audience's register, and
opening with a title and summary. Several scenarios introduce the **Harborlight Shipment Tracker** --
a small logistics company's order-to-delivery notification system -- the running example several
later scenarios in this topic return to. Every artifact below also lives, standalone, under
`learning/artifacts/`.

---

### Worked Scenario 1: BLUF Rewrite

**Context**: Exercises co-01. An on-call engineer investigates a spike in Shipment API p99 latency,
then sends a status update to the Shipment Platform team's channel. The update narrates the
investigation in the order it happened -- symptom, then three ruled-out hypotheses, then the actual
cause -- and buries the one thing the team actually needs to know, and the one thing the engineer
needs from them, in the last sentence.

**Before**:

> Was looking into the p99 latency spike on `/shipments/{id}` since about 09:40. First checked
> whether it was a DB issue -- ran `EXPLAIN ANALYZE` on the main query, looked fine, indexes are being
> used. Then checked whether it was the ParcelLink carrier lookup timing out -- checked their status
> page, no incident reported there either. Eventually noticed the connection pool metrics and it
> looks like we're maxing out `shipment_db`'s connection pool during the 09:00-10:00 order-ingestion
> burst, so requests are queueing for a free connection. I think we should probably bump the pool
> size, but I'd want someone to sign off on that since it touches a shared config.

**After (BLUF)**:

> **Decision needed today: approve raising `shipment_db`'s connection-pool size from 20 to 40.** Root
> cause of this morning's p99 latency spike: the pool maxes out during the 09:00-10:00 order-ingestion
> burst, so requests queue for a free connection instead of failing fast or running normally. DB query
> plan and the ParcelLink carrier lookup are both ruled out -- neither shows any regression.

**Verify**: the decision ("raise the pool size to 40") and the ask ("approve... today") both appear
in the literal first sentence -- satisfying co-01's rule.

**Key takeaway**: The investigation narrative did not disappear in the rewrite -- it moved below the
decision, where a reader who needs it can still find it, instead of standing between the reader and
the one sentence they actually needed.

**Why It Matters**: A reader scanning a busy channel either reads the "before" version to the end (and
resents the three ruled-out hypotheses standing between them and the ask) or stops partway through and
never sees the ask at all. The "after" version gets a decision the same day precisely because the
reader does not have to excavate it.

---

### Worked Scenario 2: Inverted-Pyramid Restructure

**Context**: Exercises co-02. A proposal to move `shipment_db` from a single Postgres instance to a
primary plus two read replicas is written in discovery order: it opens with a week of investigation
notes, then a load-test appendix, and only in its final section states the actual proposal.

**Reasoning**: co-01 fixes a document's first sentence; co-02 is the same discipline applied to the
whole document. A reader who reads only the first two paragraphs of the "before" version learns
nothing about what is being proposed -- both paragraphs are investigation narrative. The rewrite
promotes the conclusion to the top and lets the investigation notes and load-test appendix sink to
the bottom, in the order a reader is actually likely to need them.

**Decision artifact**:

> **Proposal: add two Postgres read replicas for `shipment_db`.** Read-heavy endpoints (`GET
/shipments/{id}`, `GET /shipments?customer_id=`) currently compete with order-ingestion writes for
> the same connection pool and the same I/O, which is the direct cause of this morning's latency
> spike (Scenario 1). Routing reads to two replicas separates that contention with no change to write
> behavior.
>
> **What this costs**: replica lag (typically under 200ms in our load test, Appendix B) means a read
> immediately following a write may occasionally see slightly stale data -- acceptable for shipment
> status display, not acceptable for the order-confirmation write path, which stays on the primary.
>
> _(Appendix A: a week of investigation notes. Appendix B: load-test results.)_

**Verify**: a reader who stops after the first two paragraphs already has the proposal, the reason,
and the one cost that matters -- satisfying co-02's rule that a reader who stops early still has the
answer.

**Key takeaway**: Nothing in the appendices was deleted -- inverted pyramid is a reordering
discipline, not a cutting discipline (that is co-14's job). The investigation notes still exist for
the reader who wants them, just no longer standing between every reader and the conclusion.

**Why It Matters**: A proposal document is read by people with very different appetites for detail --
a reviewer approving the trade-off needs the first two paragraphs; an engineer implementing it needs
the appendices too. Ordering by importance serves both readers from the same document, instead of
forcing the second reader's needs onto the first.

---

### Worked Scenario 3: Thirty-Second Skim Test

**Context**: Exercises co-03. Before shipping a short design note proposing a new `shipment_delayed`
notification type, the author runs it through the skim test: read only the headings, the bolded
phrases, and the first sentence of each paragraph, nothing else, and see what comes out.

**Decision artifact** (raw document text, as the author would ship it):

```markdown
## Proposal: add a `shipment_delayed` notification type

**Decision: add a new notification type, `shipment_delayed`, sent once a shipment's ETA slips more
than 24 hours past its original estimate.**

### Why now

Customer support tickets tagged "where is my order" have grown 30% quarter over quarter...

### What changes

The Notification Worker gains one new event type and one new template...

**Next action: Notification Worker owner (Priya) reviews the template copy by Friday.**
```

**Skim-only pass** (headings + bold + first sentences only): "Decision: add a new notification type,
`shipment_delayed`... Next action: Notification Worker owner (Priya) reviews the template copy by
Friday." Nothing else is read.

**Verify**: the skim-only pass above, produced by reading nothing but headings, bold text, and first
sentences, yields both the decision and the next action -- satisfying co-03's rule.

**Key takeaway**: The skim test is not a metaphor -- it is a literal exercise the author can run on
their own document before shipping it: read only what a skimmer would read, and check whether that
subset alone still carries the point.

**Why It Matters**: Most readers skim before they decide whether to read fully. A document that only
communicates its decision in paragraph four of unbolded prose has effectively hidden that decision
from most of its actual audience, no matter how clear paragraph four turns out to be once someone
finally reaches it.

---

### Worked Scenario 4: What-Why-Verify PR Description

**Context**: Exercises co-09. A PR adds retry-with-backoff to the Carrier Adapter's calls to the
external ParcelLink API, which had been failing intermittently under load with no retry at all.

**Decision artifact**:

> **What**: adds exponential backoff (3 retries, 200ms/400ms/800ms) to `CarrierAdapter.get_status()`,
> the function that calls ParcelLink's `/tracking` endpoint.
>
> **Why**: ParcelLink's API returns transient 503s under their own load spikes (roughly 2% of calls
> during their peak hours, per their own status page's historical incident log). Today those 503s
> propagate straight to the customer-facing shipment-status page as an error; a short retry absorbs
> almost all of them.
>
> **How verified**: added a test that mocks ParcelLink returning two 503s then a 200, confirming the
> adapter retries and eventually returns the successful result; ran the existing adapter test suite
> unchanged (all passing).
>
> **Where to look first**: `carrier_adapter/retry.py`, the backoff-and-retry loop itself -- everything
> else in the diff is unchanged call sites threading the new `retries=3` parameter through.

**Verify**: all four elements -- what, why, how verified, where to look first -- are present, and the
"where to look first" line names the one file that carries the actual new logic -- satisfying co-09's
rule that a reviewer knows where to start.

**Key takeaway**: The "where to look first" line is what turns a PR description from a changelog
entry into a reviewing aid -- it tells a reviewer facing an eight-file diff exactly which one file
deserves close attention.

**Why It Matters**: Without a "where to look first" pointer, a reviewer facing this same diff would
likely spend equal time on the mechanical call-site changes and the one file containing genuinely new
retry logic -- the file most likely to hide a real bug (an off-by-one in the retry count, a missing
backoff cap) gets the same shallow read as the boilerplate around it.

---

### Worked Scenario 5: Cut Hedging and Filler

**Context**: Exercises co-14. A paragraph explaining why the Shipment Platform team is evaluating a
new event bus is loaded with hedges and filler that dilute every claim it makes.

**Before**:

> So I think we're probably going to need to look at replacing our current queue setup at some point,
> because it's honestly just kind of struggling to keep up, and I sort of feel like we're basically
> going to hit a wall with it eventually if traffic keeps growing the way it has been. I mean, it's
> not really broken yet, but I think it's worth maybe starting to look at alternatives sort of soon.

**After**:

> Our current queue cannot sustain projected traffic growth. At current growth rates, we hit its
> throughput ceiling within two quarters. We are evaluating alternatives now, before that ceiling
> becomes an incident.

**Verify**: the edited paragraph drops from 76 words to 34, every hedge (I think, sort of, kind of,
honestly, basically, maybe) and filler word (just, really) is removed, and each of the three
remaining sentences reads as a complete, standalone claim -- satisfying co-14's rule.

**Key takeaway**: Nothing false was removed and nothing new was added -- every claim in the "after"
version was already present in the "before" version, just buried under words that made it sound less
certain than the author actually was.

**Why It Matters**: A reader (especially one deciding whether to fund a migration project) reads
hedged language as a signal of the author's own uncertainty about the underlying facts, not just
about the writing style -- "I think we're probably going to need to" reads as far less actionable
than "we hit its throughput ceiling within two quarters," even though both sentences describe the
same underlying situation.

---

### Worked Scenario 6: RFC 2119 Keyword Precision

**Context**: Exercises co-13. The Shipment Event Schema contract -- the document downstream consumers
of Harborlight's shipment events are supposed to follow -- uses vague, inconsistent language for its
requirements, and two different consumer teams have implemented the schema two different ways as a
result.

**Before**:

> The `event_id` field should probably be unique per event. Consumers should ideally be able to handle
> duplicate deliveries gracefully, since our queue doesn't guarantee exactly-once delivery. New fields
> might get added to the payload over time, so you shouldn't assume the field list you see today is the
> complete list forever.

**After (RFC 2119)**:

> Every event MUST carry a globally unique `event_id`. Consumers MUST implement idempotent processing
> keyed on `event_id`, because the underlying queue provides at-least-once delivery, not
> exactly-once. Consumers MUST NOT assume the payload's field list is closed -- new optional fields
> MAY be added in the future, and a conformant consumer SHOULD ignore fields it does not recognize
> rather than rejecting the event.

**Verify**: every requirement now carries an ALL-CAPS RFC 2119 keyword (MUST, MUST NOT, SHOULD, MAY)
rather than a vague qualifier like "should probably" or "shouldn't assume" -- satisfying co-13's rule
that each requirement's strength is unambiguous.

**Key takeaway**: "Should probably be unique" and "MUST carry a globally unique `event_id`" describe
the identical intended contract -- the rewrite did not change what the schema requires, only how
unambiguously that requirement is stated.

**Why It Matters**: The two consumer teams' divergent implementations are the direct, predictable
cost of the "before" version's ambiguity -- one team read "should probably be unique" as a strong
guarantee and skipped deduplication logic; the other read it as a soft suggestion and built dedup
logic anyway. RFC 2119 keywords exist precisely to prevent two competent readers from reaching two
different conclusions about the same sentence.

---

### Worked Scenario 7: Audience Register Match

**Context**: Exercises co-15. Following up on the duplicate-notification issue the Notification
Worker exhibited last quarter (the incident this topic's capstone documents in full), the Shipment
Platform team lead writes two versions of the same update: one for the VP of Engineering, one for the
engineer who will implement the fix.

**Decision artifact**:

> **Executive version**: Last quarter, a subset of customers received duplicate shipment
> notifications after a routine worker restart. No data was lost and no customer action was required,
> but it eroded trust in our SMS/email channel. We are adding a safeguard (an idempotency check) that
> makes this class of failure structurally impossible going forward, shipping this sprint, at no
> added infrastructure cost.
>
> **Engineer version**: The Notification Worker consumes from an at-least-once queue and processes
> each message without checking whether it already ran -- a consumer-group rebalance during a
> deployment restart replayed roughly 340 already-processed messages, and every one fired a duplicate
> SMS/email. The fix: a Redis-backed idempotency cache keyed on the event's `event_id` (co-13's schema
> field), with a 48-hour TTL comfortably longer than any plausible replay window. See the ADR and RFC
> under this topic's capstone for the full design.

**Verify**: the executive version contains no queue-internals vocabulary (consumer group, rebalance,
TTL) and frames the fix in terms of trust and cost; the engineer version names the exact mechanism and
the specific data structure -- each version's vocabulary and detail level is demonstrably different
and driven by what that audience needs to do next, satisfying co-15's rule.

**Key takeaway**: Both versions describe the same incident and the same fix -- the difference is
entirely in vocabulary, depth, and framing, calibrated to what each reader needs to decide or do.

**Why It Matters**: Handing the engineer version to the VP would bury the one sentence they actually
need ("no customer action required, shipping this sprint") under queue-internals vocabulary that
does not help them decide anything; handing the executive version to the implementing engineer would
leave them with nothing concrete enough to start building from.

---

### Worked Scenario 8: Title and TL;DR First

**Context**: Exercises co-01 and co-03. A design note proposing a one-time backfill of historical
shipment notifications (customers who never received their original "shipped" SMS due to an earlier
bug) is otherwise well-organized but opens directly into background paragraphs with no title or
summary at all.

**Decision artifact** (raw document text, as the author would ship it):

```markdown
# Backfill Historical Shipment Notifications

**TL;DR**: send a one-time, opt-out backfill SMS to the ~1,200 customers affected by last month's
notification-delivery bug, informing them their shipment already arrived. Shipping Thursday, pending
legal's sign-off on the message copy.

## Background

Last month's bug (see postmortem, linked) silently dropped the "shipped" notification for a subset
of orders placed between March 3-March 9...
```

**Verify**: reading the TL;DR alone -- without the Background section beneath it -- conveys the
complete outcome: what will happen, to whom, and when, pending what -- satisfying the combined
co-01/co-03 rule that the summary alone conveys the outcome.

**Key takeaway**: A title plus a two-sentence TL;DR turns a document that used to require reading the
Background section to understand its point into one whose point is available before a reader commits
to reading further at all.

**Why It Matters**: A document with no title is hard to find again later and hard to reference by
name in a follow-up conversation; a document with no TL;DR forces every future reader to re-derive
the outcome from the Background section, even readers who only need to confirm the decision already
shipped. Both costs compound every time the document gets reopened.

---

← Previous: [Overview](./overview.md) · Next: [Intermediate Scenarios](./intermediate.md) →
