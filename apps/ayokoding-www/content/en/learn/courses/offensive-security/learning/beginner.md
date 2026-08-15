---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

> **Authorized lab target only.** These examples teach engagement decisions using a self-owned,
> isolated lab and recorded fixtures. They are not instructions for testing public or third-party systems.

## Scope and method

### Worked Example 1: Record authorization

Write `owner`, `authorized tester`, `localhost target`, dates, and a stop condition before opening a
tool. This makes the authorization scope reviewable. **Takeaway**: permission is an explicit input,
not an assumption. (co-01)

### Worked Example 2: Mark boundaries

Put `localhost` in scope and every other host out of scope. **Takeaway**: a narrow target list protects
everyone outside the lab. (co-01, co-02)

### Worked Example 3: Draft rules of engagement

Use the capstone's rules-of-engagement template and obtain owner sign-off before evidence review.
**Takeaway**: rules precede testing. (co-02)

### Worked Example 4: Plan disclosure

Route a synthetic finding to its fictional owner with a remediation window. **Takeaway**: responsible
disclosure fixes a weakness without exposing others. (co-03)

### Worked Example 5: Verify isolation

Confirm the fixture says `localhost` and that no route or shared production data is involved.
**Takeaway**: a vulnerable lab must be contained. (co-31)

### Worked Example 6: Identify the local lab

Name a locally run Juice Shop or DVWA instance without publishing it or exposing it externally.
**Takeaway**: deliberately vulnerable software belongs only in an owned lab. (co-31)

### Worked Example 7: Order the lifecycle

Arrange scope → observe → analyze → document → clean up. **Takeaway**: a bounded engagement has a
start and a safe ending. (co-04)

### Worked Example 8: Name PTES phases

Match pre-engagement, intelligence gathering, threat modeling, vulnerability analysis, exploitation,
post-exploitation, and reporting to safe lab-only decisions. **Takeaway**: methodology never replaces
authorization. (co-05)

### Worked Example 9: Map the kill chain

Annotate the seven Cyber Kill Chain stages and identify where a defender can interrupt one. **Takeaway**:
breaking any stage reduces harm. (co-06)

### Worked Example 10: Choose a defensive interruption

For a synthetic delivery event, choose filtering, MFA, or segmentation as an interruption. **Takeaway**:
the model serves defense, not escalation. (co-06)

### Worked Example 11: Separate tactic from technique

Label a tactic as a goal and a technique as a method in a fictional ATT&CK mapping. **Takeaway**: precise
language makes a report actionable. (co-07)

### Worked Example 12: Interpret reconnaissance

Classify a recorded lab inventory as reconnaissance without collecting new data. **Takeaway**: record
only the evidence your scope permits. (co-07, co-08)

### Worked Example 13: Classify passive evidence

Identify a lab owner's documentation as passive evidence because no target interaction occurs.
**Takeaway**: passive does not mean permission-free outside the lab. (co-08)

### Worked Example 14: Classify active evidence

Identify an owner-approved local health check as active contact. **Takeaway**: active work needs the
clearest boundary. (co-08)

### Worked Example 15: Bound OSINT

Use only a self-owned lab README and synthetic public profile. **Takeaway**: do not research people or
organizations outside the written scope. (co-09)

## Synthetic discovery evidence

Run `python3 code/parse_lab_evidence.py` to parse the supplied static fixture; it opens no socket.

### Worked Example 16: Read host discovery

Interpret `localhost` in the fixture as a known, live lab host. **Takeaway**: recorded evidence is
enough for this exercise. (co-10)

### Worked Example 17: Inventory a port record

Read the fixture's synthetic service row and list it in a report. **Takeaway**: discovery evidence is
not permission to probe beyond scope. (co-10, co-11)

### Worked Example 18: Compare scan categories

Annotate SYN and connect scanning as concepts using the official Nmap option reference, without running
either. **Takeaway**: know the distinction; do not apply it to an unapproved target. (co-11)

### Worked Example 19: Interpret UDP evidence

Identify a fixture entry as UDP evidence rather than issuing a UDP scan. **Takeaway**: static fixtures
make the lesson safe and repeatable. (co-11)

### Worked Example 20: Read a version label

Extract a synthetic version string from local JSON. **Takeaway**: version data supports remediation,
not opportunistic exploitation. (co-12)

### Worked Example 21: Parse local evidence in Python

Run the parser and verify it accepts only the bundled fixture. **Takeaway**: a tool should make its
safety boundary enforceable. (co-10)

### Worked Example 22: Enumerate a fixture banner

Record the fictional banner supplied with the lab. **Takeaway**: enumerate only approved evidence. (co-13)

### Worked Example 23: Map supplied application paths

List the synthetic `/login` and `/profile` paths in the fixture. **Takeaway**: an attack-surface map is
an inventory, not a license to explore elsewhere. (co-13)

### Worked Example 24: Draw a local attack surface

Map a fictional form, session, and owner check. **Takeaway**: every input and authorization decision
deserves review. (co-13, co-14)

### Worked Example 25: Classify web finding families

Match synthetic findings to injection, script handling, authentication, and authorization families.
**Takeaway**: classification guides remediation. (co-14)

### Worked Example 26: Review a recorded request

Read a redacted, pre-recorded localhost request and response as evidence; do not replay it.
**Takeaway**: evidence review can teach the boundary without creating real traffic. (co-14)
