---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

> **Authorized lab target only.** The examples below interpret intentionally vulnerable, synthetic
> local-lab evidence. They do not include usable exploit payloads, credentials, target discovery, or
> instructions for unauthorized real-world activity.

## Local web-finding models

### Worked Example 27: Describe an injection boundary

Mark where untrusted input becomes query text in a fictional local application. **Takeaway**: the
report explains the unsafe boundary and recommends parameter binding. (co-15)

### Worked Example 28: Review a detector result

Read a fixture that labels a localhost parameter as potentially injectable; validate it only through
owner-provided test evidence. **Takeaway**: automated alerts require bounded verification. (co-15)

### Worked Example 29: Protect synthetic data

Use a fixture whose rows are invented and explain why real data must never be extracted. **Takeaway**:
the minimum proof is enough. (co-15)

### Worked Example 30: Compare blind-inference concepts

Annotate boolean and timing inference at a high level without composing a request. **Takeaway**: the
defense is to separate code from data. (co-15)

### Worked Example 31: Identify reflected output risk

Mark a fictional response that reflects unsafely encoded input. **Takeaway**: context-aware output
encoding prevents script interpretation. (co-16)

### Worked Example 32: Identify stored-output risk

Trace a synthetic comment from storage to a rendered view. **Takeaway**: validate and encode at the
right boundary. (co-16)

### Worked Example 33: Review a safe XSS fixture

Read a placeholder token such as `[unsafe-script-content-redacted]`, not executable script.
**Takeaway**: a report can prove the class without spreading a payload. (co-16)

### Worked Example 34: Recognize excessive attempts

Interpret a local audit log with repeated failed fictional logins. **Takeaway**: rate limiting and MFA
reduce authentication abuse. (co-17)

### Worked Example 35: Distinguish credential-stuffing

Contrast reused credentials with guessing in a scenario card. **Takeaway**: detection and remediation
need an accurate label. (co-17)

### Worked Example 36: Recognize spraying patterns

Identify the one-secret/many-account pattern in synthetic logs. **Takeaway**: protect users without
testing passwords. (co-17)

### Worked Example 37: Explain a missing rate limit

Record the absent control and propose a bounded retry policy. **Takeaway**: a defensive fix is more
valuable than attempting more logins. (co-17)

### Worked Example 38: Identify an IDOR symptom

Compare synthetic subject and record-owner IDs in a fixture. **Takeaway**: every object access needs
an ownership check. (co-18)

### Worked Example 39: Identify vertical authorization risk

Read a fictional route-to-role mismatch. **Takeaway**: server-side authorization must not trust UI
visibility. (co-18)

### Worked Example 40: Identify horizontal authorization risk

Read a fictional same-role ownership mismatch. **Takeaway**: peer data needs an object-level policy.
(co-18)

### Worked Example 41: Explain an intercepting proxy

Diagram the proxy as a lab-only observer between a local browser and local app. **Takeaway**: proxy
tools are for authorized inspection, never public interception. (co-19)

### Worked Example 42: Redact a request record

Remove cookies and secrets from a supplied request before attaching it to a report. **Takeaway**: evidence
must not create a second exposure. (co-19)

### Worked Example 43: Compare intended and received fields

Use the bundled request-diff fixture to see a changed local form field. **Takeaway**: server validation
must enforce policy independently of clients. (co-20)

### Worked Example 44: Explain replay risk safely

Annotate why a recorded request must not be replayed beyond the local lab. **Takeaway**: a report cites
the unsafe assumption and corrective control, not a repeatable attack sequence. (co-20)

### Worked Example 45: Name framework components

Label exploit, payload, and options as framework vocabulary in a diagram. **Takeaway**: names improve
communication; the course does not run framework modules. (co-21)

### Worked Example 46: Bound a framework simulation

Use a static successful-session record from a fictional local VM. **Takeaway**: simulated evidence
teaches impact without delivering operational instructions. (co-21)

### Worked Example 47: Contrast connection directions

Compare reverse and bind shell concepts in a non-operational diagram. **Takeaway**: segmentation and
egress control reduce post-compromise movement. (co-22)

### Worked Example 48: Describe post-exploitation risk

Read a redacted capability list, with no commands or session access. **Takeaway**: contain and report
the risk rather than extending access. (co-22)

### Worked Example 49: Identify an elevation precondition

Mark a fictional local misconfiguration as a privilege-escalation finding. **Takeaway**: patching and
least privilege close the path. (co-23)

### Worked Example 50: Review a hardening checklist

Compare local configuration facts with a baseline. **Takeaway**: enumeration for the lab ends at a
remediation decision. (co-23)

### Worked Example 51: Classify a synthetic hash

Recognize a deliberately fake hash marker and record no secret value. **Takeaway**: use modern salted
password storage. (co-24)

### Worked Example 52: Explain dictionary risk

Explain why weak passwords are vulnerable using a story card, without trying candidate passwords.
**Takeaway**: length, uniqueness, MFA, and rate limits matter. (co-24)

### Worked Example 53: Compare password-recovery models

Contrast dictionary, exhaustive, and precomputed-table concepts. **Takeaway**: salt and modern hashes
raise attacker cost. (co-24)

### Worked Example 54: Show salt's purpose

Compare two synthetic salted records with the same fictional password label. **Takeaway**: salts prevent
identical inputs producing reusable lookup entries. (co-24)
