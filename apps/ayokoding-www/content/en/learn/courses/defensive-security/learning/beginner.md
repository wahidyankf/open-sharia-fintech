---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

> **Safe lab boundary.** Every command reads this course's synthetic files only. Do not replace them with production logs, customer data, or a target you do not own and authorize.

## Worked examples

### Example 1: Blue, Red, and Purple Roles

**What you will do.** Make one observable, defensive decision for `co-01` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py roles
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-01)

### Example 2: Choose Events Worth Logging

**What you will do.** Make one observable, defensive decision for `co-02` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-02)

### Example 3: Parse a Raw Lab Log

**What you will do.** Make one observable, defensive decision for `co-06` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-06)

### Example 4: Centralize Synthetic Telemetry

**What you will do.** Make one observable, defensive decision for `co-03` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py bulk
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-03)

### Example 5: Trace a SIEM Flow

**What you will do.** Make one observable, defensive decision for `co-04` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-04)

### Example 6: Prepare OpenSearch Bulk Data

**What you will do.** Make one observable, defensive decision for `co-04` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py bulk
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-04)

### Example 7: Read a Recon Dashboard Timeline

**What you will do.** Make one observable, defensive decision for `co-05` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py timeline
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-05)

### Example 8: Normalize Two Log Shapes

**What you will do.** Make one observable, defensive decision for `co-06` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-06)

### Example 9: Recognize a Signature Detection

**What you will do.** Make one observable, defensive decision for `co-13` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-13)

### Example 10: Compare Signature and Anomaly Signals

**What you will do.** Make one observable, defensive decision for `co-13` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-13)

### Example 11: Read a Suricata Rule Shape

**What you will do.** Make one observable, defensive decision for `co-13` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-13)

### Example 12: Identify Endpoint Telemetry

**What you will do.** Make one observable, defensive decision for `co-14` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-14)

### Example 13: Extend an Endpoint View

**What you will do.** Make one observable, defensive decision for `co-14` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-14)

### Example 14: Treat Detections as Code

**What you will do.** Make one observable, defensive decision for `co-07` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py verify
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-07)

### Example 15: Write a Failed-Login Sigma Rule

**What you will do.** Make one observable, defensive decision for `co-08` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-08)

### Example 16: Inspect Sigma Rule Structure

**What you will do.** Make one observable, defensive decision for `co-09` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py detect
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-09)

### Example 17: Keep Sigma Portable

**What you will do.** Make one observable, defensive decision for `co-08` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py bulk
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-08)

### Example 18: Separate ATT&CK Tactic from Technique

**What you will do.** Make one observable, defensive decision for `co-11` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-11)

### Example 19: Check the Current Enterprise Tactic Set

**What you will do.** Make one observable, defensive decision for `co-11` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-11)

### Example 20: Map a Detection to ATT&CK

**What you will do.** Make one observable, defensive decision for `co-10` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-10)

### Example 21: Name IOC Types

**What you will do.** Make one observable, defensive decision for `co-21` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-21)

### Example 22: Match an IOC in Lab Events

**What you will do.** Make one observable, defensive decision for `co-21` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-21)

### Example 23: Ingest a Small Intelligence List

**What you will do.** Make one observable, defensive decision for `co-22` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py hunt
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-22)

### Example 24: Compare TTPs with Atomic IOCs

**What you will do.** Make one observable, defensive decision for `co-22` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py coverage
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-22)

### Example 25: Map Work to CSF Functions

**What you will do.** Make one observable, defensive decision for `co-31` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-31)

### Example 26: Place Govern Around the Work

**What you will do.** Make one observable, defensive decision for `co-31` against original synthetic telemetry; the fixture is never sent to a remote service.

```sh
# => Reads only bundled synthetic telemetry; this command opens no socket.
python3 code/blue_lab.py ir
```

**Key takeaway.** A defensive decision is useful only when another analyst can reproduce it from bounded evidence and explain its safety boundary.

**Why it matters.** Security operations improve when an analyst can repeat a decision from local, reviewable evidence. This exercise turns the concept into an observable check that supports review, tuning, and handoff. Because its inputs are synthetic and self-owned, repeating it cannot affect a production system or disclose another person's telemetry while still rehearsing professional practice. (co-31)
