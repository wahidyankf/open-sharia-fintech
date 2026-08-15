---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

> **Safe lab boundary.** Every command reads this course's synthetic files only. Do not replace them with production logs, customer data, or a target you do not own and authorize.

## Worked examples

### Example 27: Detect a Suspicious Request Pattern

**What you will do.** Make one observable, defensive decision for `co-08` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-08)

### Example 28: Test a Rule Against Benign Traffic

**What you will do.** Make one observable, defensive decision for `co-12` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-12)

### Example 29: Measure the False-Positive Trade-Off

**What you will do.** Make one observable, defensive decision for `co-12` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-12)

### Example 30: Tune a Failed-Login Threshold

**What you will do.** Make one observable, defensive decision for `co-12` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-12)

### Example 31: Detect Reflected Script Evidence

**What you will do.** Make one observable, defensive decision for `co-08, co-10` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-08, co-10)

### Example 32: Detect a Failed-Login Burst

**What you will do.** Make one observable, defensive decision for `co-08` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-08)

### Example 33: Order the Pyramid of Pain

**What you will do.** Make one observable, defensive decision for `co-23` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-23)

### Example 34: Prefer Durable Behavioral Evidence

**What you will do.** Make one observable, defensive decision for `co-23` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-23)

### Example 35: Write a Hunt Hypothesis

**What you will do.** Make one observable, defensive decision for `co-20` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-20)

### Example 36: Run a Hypothesis-Driven Hunt

**What you will do.** Make one observable, defensive decision for `co-20` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-20)

### Example 37: Pivot from One IOC

**What you will do.** Make one observable, defensive decision for `co-20` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-20)

### Example 38: Write a Safe YARA Shape

**What you will do.** Make one observable, defensive decision for `co-24` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-24)

### Example 39: Read YARA Strings and Condition

**What you will do.** Make one observable, defensive decision for `co-24` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-24)

### Example 40: Perform Static Sample Review

**What you will do.** Make one observable, defensive decision for `co-25` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-25)

### Example 41: Describe Sandboxed Dynamic Review

**What you will do.** Make one observable, defensive decision for `co-25` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-25)

### Example 42: Map an Incident Response Lifecycle

**What you will do.** Make one observable, defensive decision for `co-15` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-15)

### Example 43: Prepare an Incident Playbook

**What you will do.** Make one observable, defensive decision for `co-16` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-16)

### Example 44: Scope an Incident from Telemetry

**What you will do.** Make one observable, defensive decision for `co-17` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-17)

### Example 45: Separate Precursors from Indicators

**What you will do.** Make one observable, defensive decision for `co-17` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-17)

### Example 46: Contain a Fictional Lab Incident

**What you will do.** Make one observable, defensive decision for `co-18` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-18)

### Example 47: Eradicate a Lab Foothold

**What you will do.** Make one observable, defensive decision for `co-18` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-18)

### Example 48: Recover a Lab Service

**What you will do.** Make one observable, defensive decision for `co-18` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-18)

### Example 49: Preserve a Synthetic Evidence Record

**What you will do.** Make one observable, defensive decision for `co-18` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-18)

### Example 50: Write a Blameless Lessons-Learned Note

**What you will do.** Make one observable, defensive decision for `co-19` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-19)

### Example 51: Apply Zero-Trust Tenets

**What you will do.** Make one observable, defensive decision for `co-26` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hardening
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-26)

### Example 52: Separate Policy Decision and Enforcement

**What you will do.** Make one observable, defensive decision for `co-26` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hardening
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-26)
