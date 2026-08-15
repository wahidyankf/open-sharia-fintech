---
title: "Correlation and Tuning Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

> **Safe lab boundary.** The correlations below are evaluated only over course-authored rows. They model
> analyst review of a fictional sequence; they are not instructions for accessing, testing, or targeting a system.

## Worked examples

### Example 27: Model a Failed-Then-Success Chain

**What you will do.** Evaluate the lab's invented sequence: repeated failed actions from one documentation address, followed by a success.

```sh
# => Correlates only the bundled fictional rows and prints a review prompt.
python3 code/detection_lab.py correlate
```

**Key takeaway.** Correlation adds context by requiring a defined relationship among events.

**Why it matters.** One failure may be routine, while a bounded sequence may deserve review. Defining the sequence in tests prevents vague “suspicious activity” rules that analysts cannot explain or tune. (co-09)

### Example 28: Set a Bounded Frequency Window

**What you will do.** Inspect the local correlation rule's small frequency and timeframe values as a teaching contract.

```sh
# => Reads XML attributes locally and never changes a ruleset.
python3 code/detection_lab.py rules
```

**Key takeaway.** Frequency without a timeframe is not a reproducible correlation condition.

**Why it matters.** The window controls both sensitivity and alert volume. A stated value makes the trade-off reviewable and lets a future maintainer decide whether the fixture still represents expected behavior. (co-10)

### Example 29: Correlate on One Synthetic Source

**What you will do.** Confirm that the lab correlates events only when their invented source field matches.

```sh
# => Compares in-memory source labels from the original training fixture.
python3 code/detection_lab.py correlate
```

**Key takeaway.** Correlation keys must be chosen deliberately and tested against unrelated events.

**Why it matters.** Joining every event in a window can manufacture a misleading story. A narrow source key demonstrates how to keep a correlation hypothesis bounded and reviewable. (co-09)

### Example 30: Explain Correlation Severity

**What you will do.** Compare the base failed-action rule with the higher-priority local correlation decision.

```sh
# => Prints fixed training severity labels derived from local rules.
python3 code/detection_lab.py correlate
```

**Key takeaway.** A sequence can justify different prioritization than any individual event.

**Why it matters.** Severity escalation should follow documented evidence, not intuition. The lab makes the rationale inspectable: a series plus a success is reviewed differently from one routine failure. (co-08, co-09)

### Example 31: Measure a Baseline False-Positive Rate

**What you will do.** Calculate the false-positive rate across pre-labeled benign local rows.

```sh
# => Uses only fixed teaching labels; no operational data is collected.
python3 code/detection_lab.py tune
```

**Key takeaway.** A rate needs a known population, a disposition label, and a stated period.

**Why it matters.** “Noisy” is not a measurable tuning requirement. Even a tiny fixture teaches that a proposed change must identify the benign population it is expected to improve. (co-11, co-23)

### Example 32: Tune a Failed-Login Threshold

**What you will do.** Compare the teaching threshold of one against three and keep the known suspicious chain detectable.

```sh
# => Computes both threshold outcomes over original in-memory samples.
python3 code/detection_lab.py tune
```

**Key takeaway.** Tune a threshold only alongside a retained true-positive test.

**Why it matters.** Raising a threshold may reduce routine alerts while also hiding the condition the rule exists to find. The local harness reports both effects so the trade-off cannot be ignored. (co-11, co-12)

### Example 33: Keep a Known Service Exception Narrow

**What you will do.** Inspect the fictional exception record and its expiry/review requirements.

```sh
# => Prints a course-local exception example without changing any allow-list.
python3 code/detection_lab.py exception
```

**Key takeaway.** An exception needs scope, reason, owner, and expiration—not an unbounded exclusion.

**Why it matters.** Allow-listing can reduce duplicate review work, but it can also hide the evidence a rule needs. Narrow records make that residual risk visible. (co-13)

### Example 34: Check a True Positive Survives Tuning

**What you will do.** Assert that the original fictional chain still produces one reviewable correlation after tuning.

```sh
# => Executes a deterministic local assertion over the bundled sequence.
python3 code/detection_lab.py correlate
```

**Key takeaway.** A tuning change is incomplete until the intended signal still has a passing test.

**Why it matters.** False-positive reductions can feel successful because the dashboard gets quieter. Preserving a true-positive fixture keeps the purpose of the detection visible during maintenance. (co-12, co-16)

### Example 35: Compare Noise Before and After

**What you will do.** Print the alert count produced by the loose and tuned local thresholds.

```sh
# => Reports counts from fixed sample labels and performs no external query.
python3 code/detection_lab.py tune
```

**Key takeaway.** Compare a tuning change with an explicit before state and a known dataset.

**Why it matters.** A percentage without its denominator can mislead a reviewer. Showing both counts and the preserved signal supports a defensible decision instead of dashboard-driven guesswork. (co-11, co-12)

### Example 36: Separate Allow-List from Blind Spot

**What you will do.** Judge whether a fictional exception is narrow enough to preserve the detection hypothesis.

```sh
# => Evaluates only a static teaching record and emits no configuration update.
python3 code/detection_lab.py exception
```

**Key takeaway.** An exception is safe only when it explains what remains observable and when it ends.

**Why it matters.** Broad exclusions often become permanent blind spots. The exercise asks for evidence and a review date so a temporary operational fact cannot silently rewrite a detection's purpose. (co-13)

### Example 37: Test a Correlation Fixture

**What you will do.** Run the focused correlation assertion separately from the full verification suite.

```sh
# => Tests the local chain only, making a correlation failure easy to locate.
python3 code/detection_lab.py correlate
```

**Key takeaway.** Focused tests make a broken correlation diagnosable before a release gate fails.

**Why it matters.** Detection packs grow over time. A targeted test helps maintainers distinguish parser regressions, rule changes, and altered fixture expectations without consulting a live SIEM. (co-16)

### Example 38: Add a Second Local Source Shape

**What you will do.** Compare an invented nonmatching source shape with the lab's accepted decoder shape.

```sh
# => Demonstrates local rejection rather than adding a real collector.
python3 code/detection_lab.py reject
```

**Key takeaway.** A new source requires its own parsing contract before it joins a correlation.

**Why it matters.** Field names that look similar can carry different meanings across sources. Treating normalization as explicit work prevents a multi-source rule from joining unrelated evidence. (co-05)

### Example 39: Join Decoder Evidence Deliberately

**What you will do.** Review which decoded fields are used by the teaching correlation and which are deliberately ignored.

```sh
# => Prints the bounded local correlation key and its fixed event sequence.
python3 code/detection_lab.py correlate
```

**Key takeaway.** Correlation joins evidence; it should not infer missing links from convenience.

**Why it matters.** Explicit keys keep an analyst's narrative grounded in data. The course's single-source join is intentionally small so readers can audit every assumption. (co-09)

### Example 40: Detect a Repeated Action

**What you will do.** Count repeated local failed actions and compare the count with the configured teaching threshold.

```sh
# => Counts only bundled failure labels in process memory.
python3 code/detection_lab.py correlate
```

**Key takeaway.** Threshold detections are count-and-window hypotheses, not universal truths.

**Why it matters.** A count that is meaningful for one service can be normal for another. Testing an explicit synthetic threshold teaches the need for environment-specific evidence. (co-10)

### Example 41: Identify a Long-Window Trade-Off

**What you will do.** Explain why increasing the lab's correlation window may find more sequences and create more unrelated joins.

```sh
# => Prints a local trade-off note; it does not wait on or query real time.
python3 code/detection_lab.py tradeoff
```

**Key takeaway.** Wider windows improve sensitivity only by accepting more correlation uncertainty.

**Why it matters.** Low-and-slow behavior can require patience, but a very wide window can turn ordinary events into a misleading chain. The right decision depends on measured local evidence. (co-10, co-12)

### Example 42: Verify a Rule Does Not Overfire

**What you will do.** Run the benign-fixture assertion after checking the correlation condition.

```sh
# => Verifies known benign local rows remain quiet under the tuned rule.
python3 code/detection_lab.py tune
```

**Key takeaway.** “Does not overfire” is a testable expectation, not a subjective dashboard impression.

**Why it matters.** A good detection protects analyst attention. Regression tests over a benign corpus make false-positive risk visible whenever a parser, threshold, or exception changes. (co-11, co-16)

### Example 43: Add Asset Criticality to Triage

**What you will do.** Apply an invented criticality label to a fictional alert while retaining the original rule evidence.

```sh
# => Joins a static local label and never accesses an asset-management platform.
python3 code/detection_lab.py triage
```

**Key takeaway.** Enrichment changes priority context, not the facts observed by a rule.

**Why it matters.** Analysts need to know why two similar alerts receive different attention. Keeping the evidence and enrichment separate avoids overstating the confidence of either. (co-20, co-19)

### Example 44: Enrich an Alert Without Contacting a Feed

**What you will do.** Add a fictional context value from a constant mapping rather than a live reputation feed.

```sh
# => Demonstrates local enrichment and performs no network lookup.
python3 code/detection_lab.py triage
```

**Key takeaway.** Enrichment can be tested locally before an owner considers external data sources.

**Why it matters.** External enrichment has privacy, freshness, and availability risks. A static training map lets readers practice how context affects triage without creating those dependencies. (co-20)

### Example 45: Route a Reviewable Alert

**What you will do.** Produce a fictional triage routing decision with evidence, uncertainty, and owner fields.

```sh
# => Prints only a local training record; it does not open a ticket or page anyone.
python3 code/detection_lab.py triage
```

**Key takeaway.** Triage routing should be repeatable from the alert and documented context.

**Why it matters.** A well-written prompt shortens review time while preventing automatic escalation from replacing judgment. The lab records what is known and what the owner must still confirm. (co-19)

### Example 46: Escalate a Fictional True Positive

**What you will do.** Define the handoff from a locally confirmed teaching alert to the incident-response foundation course.

```sh
# => Prints a tabletop-only handoff checklist without operating on a host.
python3 code/detection_lab.py triage
```

**Key takeaway.** Detection engineering hands evidence into response; it does not replace response authority.

**Why it matters.** This course stays focused on SIEM operations. Actual containment and recovery decisions belong to the incident-response practice established in `defensive-security`. (co-21)

### Example 47: Build a Severity Trend Panel

**What you will do.** Inspect the dashboard plan's severity-count panel and its question for the reviewer.

```sh
# => Reads local JSON planning data and never creates a visualization remotely.
python3 code/detection_lab.py dashboard
```

**Key takeaway.** A panel should connect a metric to a specific review question.

**Why it matters.** Alert volume alone can hide a broken decoder or noisy rule. A named question tells the reviewer what evidence to inspect when a trend changes. (co-18)

### Example 48: Build a Tuning Review Panel

**What you will do.** Inspect the false-positive tuning panel, including its benign denominator and retained-signal check.

```sh
# => Validates the original dashboard plan fields offline.
python3 code/detection_lab.py dashboard
```

**Key takeaway.** A tuning dashboard must show both noise reduction and the signal it preserves.

**Why it matters.** A quiet dashboard can mean improved precision or a disabled rule. Pairing false-positive evidence with a true-positive fixture protects against the latter interpretation. (co-18, co-23)

### Example 49: Map Rule Coverage to a Technique

**What you will do.** Read the lab's technique mapping and connect it to one tested rule rather than an abstract inventory.

```sh
# => Prints original course mapping metadata without querying a framework API.
python3 code/detection_lab.py coverage
```

**Key takeaway.** Coverage claims should link to an actual rule and its evidence corpus.

**Why it matters.** A technique matrix is valuable only when it reveals what telemetry and tests support each square. The local mapping keeps the claim small and auditable. (co-14, co-23)

### Example 50: Find a Coverage Gap in the Lab

**What you will do.** Identify a fictional behavior with no decoder/rule test and record it as a gap rather than inventing coverage.

```sh
# => Lists a course-local gap statement; no activity is generated or replayed externally.
python3 code/detection_lab.py coverage
```

**Key takeaway.** An honest gap is more useful than an untested coverage claim.

**Why it matters.** Detection engineering improves through prioritized hypotheses. Naming missing telemetry or a missing test lets a team decide whether to instrument, write, or defer a rule. (co-23)

### Example 51: Review a Rule Change for Noise Risk

**What you will do.** Read the review checklist for a fictional threshold change before accepting the new value.

```sh
# => Prints a local peer-review checklist and does not create a pull request.
python3 code/detection_lab.py change
```

**Key takeaway.** Rule review includes false-positive and false-negative risk, not only XML validity.

**Why it matters.** A syntactically valid rule can still harm an analyst queue. Requiring evidence, benign tests, retained signals, and rollback notes turns a configuration edit into an engineering decision. (co-15, co-16)

### Example 52: Verify Correlation and Tuning Together

**What you will do.** Run the full local suite after reviewing correlation and false-positive assumptions.

```sh
# => Rechecks original decoder, rules, dashboard plan, and synthetic results offline.
python3 code/detection_lab.py verify
```

**Key takeaway.** Correlation and tuning must pass together because either can invalidate the detection's purpose.

**Why it matters.** A correlation can be precise but too noisy, or quiet but incapable of finding its intended sequence. One repeatable local gate gives a maintainer evidence about both properties. (co-09, co-11, co-16)
