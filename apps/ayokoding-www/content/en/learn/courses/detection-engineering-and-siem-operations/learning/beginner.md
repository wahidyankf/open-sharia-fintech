---
title: "Decoder and Rule Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

> **Safe lab boundary.** Each command reads original synthetic files in this directory only. It never
> contacts a SIEM, host, account, or user. Do not replace the fixtures with real telemetry.

## Worked examples

### Example 1: Frame a Detection Hypothesis

**What you will do.** State a local, testable detection claim before writing XML. The invented lab asks whether a repeated failed action followed by a success needs analyst review.

```sh
# => Prints the bounded, local hypothesis; no endpoint or live event is accepted.
python3 code/detection_lab.py hypothesis
```

**Key takeaway.** A detection starts as an evidence claim, not an assumption about a person or system.

**Why it matters.** A written claim gives the decoder, rule, test fixture, and dashboard a shared purpose. It also limits overreach: a lab alert is a prompt to review synthetic evidence, not proof of identity, intent, or compromise. (co-01)

### Example 2: Inspect Invented Source Telemetry

**What you will do.** Read one invented log shape and identify its bounded fields. The fixture uses documentation-only addresses and fictional action words.

```sh
# => Lists local fixture rows and never reads a log file outside this course.
python3 code/detection_lab.py events
```

**Key takeaway.** Detection quality cannot exceed the clarity and provenance of the telemetry it receives.

**Why it matters.** Inspecting the raw shape before parsing prevents rules from silently depending on fields that do not exist. Original synthetic data lets a learner practice this discipline without exposing a customer, employee, or production service. (co-02)

### Example 3: Trace a Local Ingestion Boundary

**What you will do.** Trace the course's file-to-parser boundary without configuring a real collector. The illustrative configuration is reviewed as text, never applied.

```sh
# => Checks that the illustrative local-file configuration is present but does not load it.
python3 code/detection_lab.py config
```

**Key takeaway.** An ingestion boundary is an explicit contract between a source and its parser.

**Why it matters.** Clear boundaries prevent accidental collection expansion and make a missing event diagnosable. In a real owned lab, an operator would review collection scope separately; this course deliberately keeps the complete exercise offline. (co-03)

### Example 4: Identify Decoder Input and Output

**What you will do.** Compare one raw fictional line with the structured fields the decoder is expected to emit.

```sh
# => Parses the bundled lab line in memory and prints only its invented fields.
python3 code/detection_lab.py decode
```

**Key takeaway.** A decoder is useful when its extracted fields are named, stable, and testable.

**Why it matters.** Rules should evaluate fields rather than guess at unstructured text. Seeing the input and expected output side by side makes parser assumptions reviewable and gives later tuning a reliable surface. (co-04)

### Example 5: Write a Narrow Prematch

**What you will do.** Inspect the decoder's narrow `prematch` condition for the invented `LABAUTH` source marker.

```sh
# => Validates the required XML element locally; it does not activate a decoder.
python3 code/detection_lab.py xml
```

**Key takeaway.** A narrow precondition reduces the chance that an unrelated line reaches a decoder.

**Why it matters.** Broad parsing creates confusing fields and noisy downstream rules. Starting with an invented source marker demonstrates how a decoder can reject irrelevant local fixtures before extraction work begins. (co-04)

### Example 6: Extract a Synthetic User Field

**What you will do.** Verify that the XML's field order and the local parser agree on the fictional user value.

```sh
# => Asserts the synthetic user field is extracted from a bundled string only.
python3 code/detection_lab.py decode
```

**Key takeaway.** Field names are contracts; a rule should not compensate for an ambiguous parser.

**Why it matters.** A wrongly ordered capture can make a rule appear to work while evaluating the wrong value. Local assertions expose that failure before a rule ever reaches an owned test environment. (co-04)

### Example 7: Extract a Documentation Address

**What you will do.** Extract an address reserved for documentation from the local log line and label it as a source field.

```sh
# => Prints only synthetic RFC 5737-style training values from the fixture.
python3 code/detection_lab.py decode
```

**Key takeaway.** Extracted network fields should be treated as evidence labels, not targets to contact.

**Why it matters.** A SIEM parser makes values searchable; it does not authorize follow-up traffic. Using invented addresses keeps the distinction visible while readers practice careful field handling. (co-04)

### Example 8: Normalize an Action Value

**What you will do.** Read the normalized `action` field used by the local rule instead of matching a whole log line.

```sh
# => Shows the parser's action values without opening a socket or an external file.
python3 code/detection_lab.py decode
```

**Key takeaway.** Normalized fields make a detection's intent clearer than opaque string matching.

**Why it matters.** When a field says `failure` or `success`, reviewers can test the rule's purpose directly. That clarity is essential when later adjusting severity, thresholds, or exceptions. (co-05)

### Example 9: Review Decoder Field Order

**What you will do.** Validate that the decoder XML's `order` lists user, source address, and action in the same order as its captures.

```sh
# => Checks the original XML text and expected local parser contract.
python3 code/detection_lab.py xml
```

**Key takeaway.** Capture order is a correctness boundary, not cosmetic XML formatting.

**Why it matters.** A field-order mismatch can silently corrupt every alert that follows. Treating the decoder as code—with explicit checks—makes that risk visible before it becomes an analyst workflow problem. (co-05)

### Example 10: Reject a Nonmatching Fixture

**What you will do.** Confirm that a line without the lab marker is rejected rather than partially decoded.

```sh
# => Exercises an invented nonmatching string in memory; no live line is accepted.
python3 code/detection_lab.py reject
```

**Key takeaway.** Negative parser tests protect a rule set from accidental broadening.

**Why it matters.** A decoder that accepts every nearby format creates unreliable fields and later false positives. A small nonmatch test gives a reviewer evidence that the boundary is intentional. (co-04)

### Example 11: Compare Signature and Baseline Signals

**What you will do.** Contrast a direct failed-action match with a count-based review decision using the same local fixture.

```sh
# => Prints local signature and threshold outcomes from original sample rows.
python3 code/detection_lab.py detect
```

**Key takeaway.** A signature recognizes a condition; a baseline or threshold supplies context.

**Why it matters.** Choosing the wrong signal type can either miss a meaningful sequence or overwhelm a queue. The lab makes the trade-off concrete without claiming that its tiny dataset models production behavior. (co-06)

### Example 12: State a Rule's Evidence Requirement

**What you will do.** Read the base rule's fictional action condition and name the evidence it requires.

```sh
# => Validates rule structure in the bundled XML without deploying it.
python3 code/detection_lab.py rules
```

**Key takeaway.** Every rule should say which decoded fact must be true before it fires.

**Why it matters.** Explicit evidence requirements make tuning possible: reviewers can ask whether the field is reliable, whether the match is too broad, and which benign cases must remain quiet. (co-07)

### Example 13: Set a Reviewable Rule Level

**What you will do.** Inspect the local rule level as a triage priority, not a declaration that an incident occurred.

```sh
# => Reads the original local rule level and prints a training-only interpretation.
python3 code/detection_lab.py rules
```

**Key takeaway.** Severity orders review work; it does not establish truth.

**Why it matters.** Analysts need consistent priorities, but a level cannot replace evidence. The course uses a modest fictional level so learners practice separating urgency from certainty. (co-08)

### Example 14: Match a Failed Auth Action

**What you will do.** Evaluate the base rule against an invented failed action and observe the resulting review prompt.

```sh
# => Evaluates only local dictionaries created from the bundled fixture.
python3 code/detection_lab.py detect
```

**Key takeaway.** A simple rule should have one clear reason to match and a test that proves it.

**Why it matters.** Small rules are easier to review, map, and tune. Starting with a precise local condition builds the discipline required before combining events in a correlation rule. (co-07)

### Example 15: Keep a Benign Success Quiet

**What you will do.** Confirm that a normal successful fictional action does not satisfy the failed-action base rule.

```sh
# => Runs a negative assertion over the built-in benign local sample.
python3 code/detection_lab.py detect
```

**Key takeaway.** A negative test is as important as a matching test for a useful detection.

**Why it matters.** Alert queues fail when ordinary behavior matches an overbroad condition. This safe fixture proves the intended distinction before later frequency logic makes the rule more complex. (co-11)

### Example 16: Attach an ATT&CK Teaching Label

**What you will do.** Inspect the rule's ATT&CK label as a coverage index for the fictional scenario.

```sh
# => Prints the local mapping label; it performs no technique or emulation action.
python3 code/detection_lab.py coverage
```

**Key takeaway.** A technique label organizes detection coverage; it is not evidence of an attack.

**Why it matters.** Coverage mapping helps teams find missing detection hypotheses and discuss them consistently. It must remain coupled to tested telemetry rather than becoming a decorative tag. (co-14)

### Example 17: Read a Local Rule Group

**What you will do.** Read the dedicated training rule group and distinguish locally owned rules from vendor defaults.

```sh
# => Checks one original group name in a course-local XML file.
python3 code/detection_lab.py rules
```

**Key takeaway.** Grouping makes ownership and review scope visible in a detection repository.

**Why it matters.** Engineers must know which rules they maintain and which behavior belongs to a platform baseline. The lab's clearly named group avoids implying that it is an official vendor ruleset. (co-15)

### Example 18: Test Parsed Fields Offline

**What you will do.** Run the parser tests that assert expected fictional user, source, and action values.

```sh
# => Executes deterministic local assertions and reports no telemetry externally.
python3 code/detection_lab.py decode
```

**Key takeaway.** Decoder testing should protect the field contract before rule testing begins.

**Why it matters.** A successful alert test can mask a broken parser if both expectations are vague. Separate parser assertions make the failure location obvious and keep maintenance costs lower. (co-16)

### Example 19: Separate Rule Text from Rule Behavior

**What you will do.** Inspect XML and then evaluate the equivalent teaching behavior in the local harness.

```sh
# => Verifies both course-authored XML markers and offline behavior assertions.
python3 code/detection_lab.py verify
```

**Key takeaway.** Configuration review and behavior review answer different questions and need both tests.

**Why it matters.** Text can look plausible while behavior is wrong, and a passing harness can hide an unreviewed configuration change. Pairing the two checks supports detection-as-code practice. (co-15, co-16)

### Example 20: Record a Detection Change

**What you will do.** Read the course's change-record convention before proposing a fictional rule adjustment.

```sh
# => Prints a local change-record checklist; it does not call version-control services.
python3 code/detection_lab.py change
```

**Key takeaway.** A change needs intent, tests, reviewer, and rollback evidence—not merely edited XML.

**Why it matters.** Detection-as-code makes future tuning explainable. Even in a tiny lab, recording the reason for a threshold or exception prevents untraceable alert behavior. (co-15)

### Example 21: Classify a Triage Prompt

**What you will do.** Classify a local alert as a review prompt with evidence, uncertainty, and an owner.

```sh
# => Prints a fictional triage record derived from synthetic alerts only.
python3 code/detection_lab.py triage
```

**Key takeaway.** Triage turns an alert into a bounded decision, not an automatic accusation.

**Why it matters.** Useful detection engineering considers what an analyst can do next. A clear prompt reduces unnecessary escalation while preserving uncertainty for the owner to resolve. (co-19)

### Example 22: Add Asset Context Locally

**What you will do.** Add an invented asset-criticality value from a local mapping, not a live inventory system.

```sh
# => Joins only in-memory training labels and does not query an asset service.
python3 code/detection_lab.py triage
```

**Key takeaway.** Enrichment should explain prioritization and preserve its source and limits.

**Why it matters.** A high-priority asset may justify faster review, but enrichment can be stale or wrong. A local example makes the dependency visible without collecting inventory data. (co-20)

### Example 23: Inspect a Dashboard Panel Plan

**What you will do.** Inspect the original dashboard-plan JSON and identify the questions its panels answer.

```sh
# => Reads a local planning document; it does not import or alter a dashboard.
python3 code/detection_lab.py dashboard
```

**Key takeaway.** A dashboard is a set of review questions, not a wall of unprioritized charts.

**Why it matters.** Intentional panels reveal alert volume, severity, and tuning outcomes. Planning fields first helps prevent dashboards from becoming decorative rather than operationally useful. (co-18)

### Example 24: Count Local Alert Severities

**What you will do.** Count fictional alert levels to support a small dashboard metric.

```sh
# => Aggregates the bundled synthetic outcomes entirely in process memory.
python3 code/detection_lab.py dashboard
```

**Key takeaway.** A metric is meaningful only when its population and review decision are explicit.

**Why it matters.** Counting levels can reveal a sudden change in rule behavior, but it cannot diagnose root cause alone. The next step is to inspect evidence and tests, not to adjust a threshold reflexively. (co-18)

### Example 25: Name a False-Positive Assumption

**What you will do.** State why one isolated synthetic failure remains below the review threshold.

```sh
# => Calculates the teaching fixture's false-positive rate from fixed local labels.
python3 code/detection_lab.py tune
```

**Key takeaway.** Tuning is an explicit hypothesis about benign behavior, recorded for later review.

**Why it matters.** An unexplained threshold becomes institutional memory that no one can challenge safely. A documented assumption lets the owner revisit it when telemetry, users, or service behavior changes. (co-11, co-12)

### Example 26: Verify the Decoder-to-Alert Path

**What you will do.** Verify the full local path from invented line through parsing, rule matching, and dashboard data.

```sh
# => Runs every offline assertion against course-local, original artifacts.
python3 code/detection_lab.py verify
```

**Key takeaway.** End-to-end evidence links parsing, detection, and review without a production deployment.

**Why it matters.** A detection pack is only maintainable when its components agree. This compact local verification gives learners a safe baseline before they practice correlation and false-positive tuning. (co-04, co-07, co-16, co-18)
