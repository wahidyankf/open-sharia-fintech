---
title: "Overview"
date: 2026-07-26T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Evaluating AI Output -- Essentials topic:
recall first, then applied judgment, then a hands-on kata, then a self-check checklist, then
elaborative-interrogation prompts that ask _why_, not just _what_. Every answer is hidden in a
`<details>` block; try each item yourself before opening it.

Every kata below is self-contained and deterministic -- hand-constructed fixtures only, no live
model call, no network, and no dependency on this topic's own worked-example or capstone code.

## Recall Q&A

Twelve short-answer questions, one per concept (`co-01` through `co-12`). Answer from memory, then
check.

**Q1 (co-01 -- why a vibe check fails).** Why can trying a feature by hand once, and having it look
right, still hide a real regression?

<details>
<summary>Answer</summary>

Because a hand-tried case is almost always the exact case the engineer already had in mind when
making the change -- it cannot possibly reveal a regression on a case the engineer did not think to
try. Only running against a fixed set of cases the engineer did NOT just author from memory can
surface that kind of silent breakage.

</details>

**Q2 (co-02 -- what "good" means, written down).** What makes a criterion good enough to count as
the "minimum unit of an eval," and what's the two-person test for it?

<details>
<summary>Answer</summary>

A criterion is good enough once you can hand it, in writing, to a second person -- along with the
model's output -- and they reach the identical pass/fail verdict you would, without asking you a
clarifying question first. If two readers can disagree given the same criterion and the same
output, the criterion isn't specific enough yet.

</details>

**Q3 (co-03 -- the ten-case dataset).** What matters more about a small eval dataset, its size or
its fixed-ness, and why?

<details>
<summary>Answer</summary>

Its fixed-ness. A dataset that changes every run cannot support a before/after comparison -- you
cannot tell whether a pass-rate change came from the prompt edit or from the inputs being different
this time. A small but FIXED set supports a real comparison; a large but constantly-regenerated set
does not.

</details>

**Q4 (co-04 -- golden outputs).** For a case with exactly one right answer, what does storing the
expected output actually buy you?

<details>
<summary>Answer</summary>

It turns the eval case into an ordinary test -- exact match (or a close variant like normalized
match) against a known-correct value, no judgment call needed, no scorer design work beyond string
comparison.

</details>

**Q5 (co-05 -- deterministic scorers).** Name the deterministic scorer family this course teaches,
and what property do they all share?

<details>
<summary>Answer</summary>

Exact match, normalized match, substring, regex, and numeric tolerance. They all share the same two
properties: they cost nothing to run (pure string/number logic, no model call) and they never
drift -- the same output always produces the same verdict, run after run, machine after machine.

</details>

**Q6 (co-06 -- schema validation as an eval).** Why is "does this structured output parse against
its schema" described as the highest-value eval per line of eval code?

<details>
<summary>Answer</summary>

Because a single, cheap structural check (are the required keys present, with the right types) can
catch an entire category of real breakage -- a malformed or incomplete structured response -- with
a few lines of code and no model call, before any content-level scoring is even needed.

</details>

**Q7 (co-07 -- pass rate as the headline number).** Why does a run's pass rate deserve to be "the
one number you compare across runs," instead of the full per-case output?

<details>
<summary>Answer</summary>

Because a single number is what makes two runs directly comparable at a glance -- "83% vs. 75%" is
immediately legible in a way a wall of per-case pass/fail lines is not. The per-case detail still
matters (co-09), but the headline number is what makes the comparison possible in the first place.

</details>

**Q8 (co-08 -- run it twice).** Why is a single run's pass rate "not yet evidence" for a stochastic
system?

<details>
<summary>Answer</summary>

Because the same input can produce a different output on a different call -- a single run's number
could just as easily be a lucky or unlucky draw as a real reflection of quality. Re-running and
comparing is the cheapest available check for whether a number is stable or was a fluke.

</details>

**Q9 (co-09 -- before-and-after comparison).** What is the eval's actual job, according to this
course -- certifying quality, or something else?

<details>
<summary>Answer</summary>

Comparing a candidate change against the current baseline -- not certifying that the system is
"good" in any absolute sense. The gate answers "did this specific change make things better or
worse," not "is this feature done."

</details>

**Q10 (co-10 -- regression cases from real bugs).** What is the ONLY legitimate source for adding a
new case to the dataset after its initial collection, according to this course's discipline?

<details>
<summary>Answer</summary>

A real, reported failure -- something a human actually hit and reported, turned into a permanent
case that fails before the fix and passes after. Speculative "what if" cases are explicitly not how
the dataset is meant to grow; growth is earned by genuine bug reports.

</details>

**Q11 (co-11 -- cost and latency in the same run).** Why record tokens, cost, and latency alongside
the pass-rate score, rather than tracking quality separately from cost?

<details>
<summary>Answer</summary>

Because a quality improvement paid for with a large cost or latency increase is a real trade-off
decision, not a free win -- if cost and latency are tracked in a separate report, or not tracked at
all, that trade-off becomes invisible at exactly the moment someone needs to decide whether to ship
the change.

</details>

**Q12 (co-12 -- knowing this gate is not enough).** Name one concrete question this ten-to-
twenty-case gate provably cannot answer, and where that question's answer lives instead.

<details>
<summary>Answer</summary>

It cannot tell you WHY a case fails (only that it did), and it cannot validate a subjective scorer
(faithfulness, tone) against measured human agreement. Both belong to
`evaluating-ai-systems-in-depth`, which runs after this course and after agents.

</details>

## Applied problems

Eight scenarios spanning the whole topic. Each describes a realistic situation without naming the
specific concept -- decide what applies and why, then check your reasoning against the worked
solution. Every scenario below is invented for this drill and does not reuse any function, fixture,
or domain from the 46 worked examples or the capstone.

**AP1.** A support-bot team ships a prompt change on a Friday after the engineer tried three
questions by hand and all three "looked good." The following Monday, a customer reports the bot now
gives a wrong answer to a question the team has fielded for months. What went wrong in the release
process, and what single artefact would have caught this before it shipped?

<details>
<summary>Worked solution</summary>

This is exactly the vibe-check trap (co-01) -- the three hand-tried questions were the ones the
engineer already had in mind, not a representative fixed set. A committed, fixed dataset (co-03)
that included the long-fielded question, scored the same way before and after (co-09), would have
caught the regression before Friday's release rather than after a customer report.

</details>

**AP2.** Two engineers review the same "criterion" for a summarization eval -- "the summary should
capture the key points" -- and independently score the same three summaries. They disagree on two
of the three. What's wrong with the criterion, and what would fix it?

<details>
<summary>Worked solution</summary>

The criterion fails the two-person test (co-02) -- "captures the key points" is a judgment call
with no operational definition, so two readers can reasonably disagree. A fixed criterion names the
SPECIFIC facts or elements that must appear (e.g. "the summary must mention the deal's dollar
amount and closing date"), turning a subjective read into something two people would score
identically.

</details>

**AP3.** A team collects exactly ten input cases for a new eval, all sampled from the SAME three
customer accounts on the SAME day. Three months later, every prompt change still passes the ten-
case gate at 100%, yet real users keep reporting new problems the gate never seems to catch. Is the
gate broken?

<details>
<summary>Worked solution</summary>

Not broken -- exactly at its documented limit (co-12). Ten cases, especially drawn from a narrow
slice (three accounts, one day), can only tell you the gate's own ten questions still pass; it says
nothing about the much larger space of real inputs the gate never sampled. The fix is not to
distrust the gate, but to grow it (co-10) every time a new real failure is reported, and to
recognise that a 100% pass rate on a narrow set is not a claim of general quality.

</details>

**AP4.** An engineer builds a scorer for a "cite exactly one product name" case using
`any(name in output for name in KNOWN_PRODUCT_NAMES)`. It passes an output that correctly cites the
product AND an output that hallucinates a plausible-sounding but entirely wrong product name from
the same list. What class of bug is this, and what's the general fix?

<details>
<summary>Worked solution</summary>

A scorer that lies (co-02, co-05) -- it checks "is ANY known name present" rather than "is the
CORRECT name for this specific case present," so it wrongly passes a confident wrong answer as long
as the wrong name happens to be a real product elsewhere in the catalog. The fix is to score against
the case's own specific expected value (an exact-match or regex scorer keyed to that case), never
against a shared pool that any plausible-looking answer could satisfy.

</details>

**AP5.** A candidate prompt raises a support-bot eval's pass rate from 80% to 88%. The team ships it
immediately. Two weeks later, a different customer segment reports a previously-reliable answer is
now consistently wrong. What check, if run before shipping, would have surfaced this regression
even though the headline number looked strictly better?

<details>
<summary>Worked solution</summary>

A per-case diff against the baseline (co-09), not just the headline pass rate. An 8-point net
improvement can still hide one or more individual regressions if enough other cases newly pass --
exactly the "helps and hurts" trap. Diffing case-by-case (`wins` vs. `regressions`) and rejecting on
ANY regression, regardless of the net number, is the check that would have caught this before
shipping.

</details>

**AP6.** A team eval-gates a batch classification feature (assign one of five fixed labels to each
input, with a single objectively correct label per input) using an LLM-as-judge subjective scorer
"rate how well the label fits, 1-5." A reviewer says this is over-engineered. Are they right, and
what should the team use instead?

<details>
<summary>Worked solution</summary>

Yes -- when the output is genuinely single-valued and deterministic downstream (a fixed label set,
one correct answer per input), an ordinary exact-match test suite is the right tool, not eval
machinery. A subjective 1-5 judge adds cost, latency, and its own reliability question to a problem
that a simple `assert predicted_label == expected_label` already solves exactly. This scenario
deliberately falls outside the twelve named concepts -- it maps instead to this course's
[Tensions & trade-offs -- when NOT to reach for this](../overview.md#tensions--trade-offs----when-not-to-reach-for-this)
section, which names exactly this "don't reach for eval machinery on a deterministic problem" case.

</details>

**AP7.** An eval runner calls the model once per case, uses `hash(case_id)` seeded per Python
process to decide mock latency for a demo, and reports a different p95 latency figure every time
the script is re-run, even with no code changes. What's the likely cause, and what's the general
fix for building reproducible mocked demo data?

<details>
<summary>Worked solution</summary>

Python's built-in `hash()` on strings is randomized per process by design (for security reasons,
unrelated to this eval), so `hash(case_id)`-derived mock data changes on every run. The general fix
is to use a hash that is stable across runs and processes -- `zlib.crc32` (or any other
non-randomized hash) on a UTF-8-encoded byte string -- exactly the technique this topic's own mocked
latency and cost figures use (co-08).

</details>

**AP8.** A team's dataset grows to 40 cases over a year, entirely because every time a customer
reports a wrong answer, an engineer adds a new case reproducing it. A new team member asks whether
this is "just accumulating cruft" and proposes periodically deleting old cases to keep the suite
fast. Is the growth pattern itself a problem?

<details>
<summary>Worked solution</summary>

No -- growth sourced entirely from real, reported failures (co-10) is exactly the intended, earned
way a dataset should grow; each case is evidence the gate is protecting against a failure mode that
genuinely happened once already. The team member's speed concern is legitimate but separate --
deterministic scorers run in microseconds each, so forty cases is not, on its own, a performance
problem; if it ever becomes one, the fix is parallelizing the run, not deleting evidence of past
real bugs.

</details>

## Code katas

Five self-contained exercises. Every kata runs on hand-constructed, in-memory data using only the
Python 3.13 standard library -- no live model call, no network, and no dependency on this topic's
own worked-example or capstone files, so every kata is runnable anywhere Python 3.13 is installed.

### Kata 1 -- Write a two-person-stable criterion, then break it on purpose

Pick any feature you know well (your own project's, or a plausible one you invent). Write a vague
one-sentence criterion ("the response should be helpful"), then write three model outputs of your
own choosing that a second reader could plausibly score differently under the vague criterion.
Rewrite the criterion so all three of your own outputs now score unambiguously the same way to any
reader -- confirm by writing out, for each output, the specific criterion clause that decides its
verdict (co-02).

### Kata 2 -- A four-field case validator, hand-built from scratch

Write `validate_case(case: dict[str, object], required_keys: set[str]) -> tuple[bool, str]` that
checks every key in `required_keys` is present in `case`, returning `(True, "ok")` or `(False,
"missing keys: [...]")` naming exactly which keys are absent, sorted. Construct three cases of your
own -- one fully valid, one missing one key, one missing two keys -- and confirm each one's
`(passed, reason)` output matches what you predicted before running it (co-03, co-04).

### Kata 3 -- A three-scorer registry dispatched by name

Implement `exact_match`, `contains_substring`, and `within_tolerance` scorers, each returning a
`(passed: bool, reason: str)` pair, and a `REGISTRY: dict[str, Callable]` mapping a name string to
each function. Build three cases of your own (each naming which scorer it uses by string key), run
every case through `REGISTRY[case["scorer"]](...)`, and confirm the right scorer fires for each case
by checking its `reason` string names the correct check (co-05).

### Kata 4 -- Detect a flaky case across two runs, from scratch

Write a mock system function that returns a fixed correct answer for every case except one, where
that one case's answer depends on a `trial: int` parameter you pass in (alternate between a correct
and an incorrect answer by trial number). Run every case through your Kata-3 registry across two
trials, collect each case's `[trial1_passed, trial2_passed]` pair, and write
`find_flaky(verdicts: dict[str, list[bool]]) -> list[str]` that returns exactly the case ids whose
two verdicts disagree. Confirm it returns exactly your one deliberately-flaky case id, sorted (co-08).

### Kata 5 -- Diff a candidate against a baseline and decide, never on pass rate alone

Construct a `baseline: dict[str, bool]` and a `candidate: dict[str, bool]` of your own choosing (at
least 6 cases each), deliberately including at least one case that regresses (`True` in baseline,
`False` in candidate) alongside at least two cases that improve (`False` to `True`), such that the
candidate's raw pass rate is numerically HIGHER than the baseline's. Write `accept_or_reject` that
rejects on any regression regardless of the net rate, and confirm your own constructed candidate is
rejected even though `sum(candidate.values()) > sum(baseline.values())` (co-07, co-09).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can explain why a hand-tried case cannot reveal a regression on a case nobody tried. (co-01)
- [ ] I can state the two-person test for a written criterion and give an example of a criterion
      that fails it. (co-02)
- [ ] I can explain why a dataset's fixed-ness matters more than its size for supporting a
      comparison. (co-03)
- [ ] I can explain what storing a golden output buys a case with exactly one right answer. (co-04)
- [ ] I can name the five deterministic scorer types this topic teaches and the one property they
      all share. (co-05)
- [ ] I can explain why schema validation is described as the highest-value eval per line of eval
      code. (co-06)
- [ ] I can explain why the pass rate, not the full per-case output, is the number you compare
      across runs. (co-07)
- [ ] I can explain why a single run's pass rate is not yet evidence for a stochastic system.
      (co-08)
- [ ] I can state the eval's actual job (comparison against a baseline, not absolute
      certification). (co-09)
- [ ] I can name the one legitimate source for growing a dataset after its initial collection.
      (co-10)
- [ ] I can explain why cost and latency belong in the SAME run report as the pass-rate score, not
      a separate one. (co-11)
- [ ] I can name at least one concrete question this gate cannot answer and where that answer lives
      instead. (co-12)

## Elaborative interrogation & self-explanation

Six prompts that ask you to explain WHY, connecting two or more concepts, rather than recall a
single fact. Write your own answer before checking the discussion.

**E1.** Why does this course insist on running the eval TWICE (co-08) before trusting a pass-rate
number, when the pass rate itself (co-07) is already a single, simple headline figure?

<details>
<summary>Discussion</summary>

The pass rate's simplicity is exactly what makes a single run dangerous to trust on its own -- one
number, computed once, gives no signal about whether it would look the same on a second try. A
stochastic system's output can vary call to call, so a single-run pass rate could be a lucky or
unlucky draw rather than a stable measurement. Running twice and checking whether any case's verdict
flips is the cheapest possible check for exactly that risk -- it converts "here is a number" into
"here is a number I have evidence is stable."

</details>

**E2.** Written criteria (co-02) and deterministic scorers (co-05) are two different ideas -- one is
prose, the other is code. Why does this course insist on both, rather than treating the scorer code
as sufficient documentation of what "good" means on its own?

<details>
<summary>Discussion</summary>

A scorer's code tells you exactly what check runs, but not necessarily WHY that check is the right
one for this case, or whether a human reviewer would agree the check is well-chosen. The written
criterion is the human-readable justification a reviewer can check the scorer's code against --
"does this regex actually implement what the criterion says it should?" -- without which a scorer
could silently drift from its intended meaning as the codebase evolves, and nobody reviewing a PR
would notice.

</details>

**E3.** Why does a regression case sourced from a real bug report (co-10) carry more weight than a
speculative case an engineer invents while writing the dataset, even if the speculative case is
well-reasoned?

<details>
<summary>Discussion</summary>

A real bug report is proof that a specific input genuinely produced a specific wrong output in the
wild -- it is not a hypothesis, it already happened. A speculative case, however well-reasoned, is a
guess about what MIGHT go wrong, and a dataset built mostly from speculation risks over-indexing on
failure modes the author happened to imagine while under-covering the ones users actually hit. This
is also why co-12's "ten cases is not coverage" limitation is honest rather than a flaw to be
engineered away with more speculative cases -- the fix that actually earns coverage is co-10's
discipline, not volume for its own sake.

</details>

**E4.** Cost and latency (co-11) are recorded in the SAME run as the pass-rate score, not in a
separate performance-testing pass. What decision does this design choice make possible that
wouldn't be possible if the two were tracked separately?

<details>
<summary>Discussion</summary>

Recording them together lets one glance answer "is this specific quality improvement worth its
specific cost," because both numbers come from the identical run against the identical dataset --
there's no risk of comparing a quality delta from one run against a cost delta from a differently-
timed, differently-scoped performance test. Tracked separately, a team could ship a 4x-cost prompt
change because the quality report looked good in isolation, only discovering the cost problem in a
totally unrelated billing review weeks later.

</details>

**E5.** This course teaches you to compare a candidate against a baseline (co-09), never to certify
absolute quality. Why is that framing -- "better or worse than before," not "good or bad" -- the
right scope for a ten-to-twenty-case gate specifically?

<details>
<summary>Discussion</summary>

A ten-to-twenty-case gate samples too small a slice of the real input space to support a confident
absolute claim like "this feature is good" -- co-12 names exactly this limit. But it samples more
than enough to answer a narrower, relative question: did THIS SPECIFIC CHANGE make these SPECIFIC
cases better or worse than they were before? Comparison is a question small data can answer
honestly; certification is a question it cannot, and pretending otherwise is exactly the overreach
this course's scope guard warns against.

</details>

**E6.** Both co-01 (a vibe check fails) and co-12 (this gate is not enough) describe a form of
"this isn't enough evidence." What's the concrete difference between the failure a vibe check
represents and the boundary co-12 names?

<details>
<summary>Discussion</summary>

A vibe check (co-01) is the ABSENCE of any fixed, repeatable evidence at all -- no dataset, no
scorer, no comparison, just one engineer's impression of one hand-picked case. Co-12's boundary is
the opposite kind of limit: it names exactly what a REAL, repeatable, fixed-dataset gate still
cannot tell you (why a case fails, whether a subjective scorer is trustworthy) even once it exists
and runs correctly. One is "you have no evidence"; the other is "you have real evidence, and here is
precisely where its authority ends" -- which is exactly why the second one is the trigger for
graduating to `evaluating-ai-systems-in-depth`, not a reason to distrust the gate this course just
taught you to build.

</details>

---

← Previous: [Capstone](../learning/capstone/overview.md)
