---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Produce a complete security assessment for a fictional receipt API. It must contain a STRIDE threat
model, an OWASP Top 10:2025 mapping, runnable mechanisms that accept valid inputs and reject altered
ones, and a filled secure-SDLC checklist. Work only with the synthetic app described here; do not scan
or test a system you do not own and have not explicitly authorized.

## Concepts exercised

- [x] STRIDE assets, entry points, threats, and mitigations (co-04, co-05)
- [x] OWASP Top 10:2025 review mapping (co-07, co-08, co-09, co-13)
- [x] Argon2id password verification and JWT integrity (co-18, co-24)
- [x] Digital-signature verification (co-19)
- [x] Dependency, secret, header, and response checks (co-26, co-27, co-28)

## Step 1: Threat-model the receipt API

| Entry point          | STRIDE threat                        | Mitigation                                               |
| -------------------- | ------------------------------------ | -------------------------------------------------------- |
| `POST /sessions`     | Spoofing through guessed credentials | Argon2id, rate policy, generic failures                  |
| `GET /receipts/{id}` | Information disclosure / elevation   | subject-object authorization predicate                   |
| `POST /receipts`     | Tampering / denial of service        | allow-list, bounded attachment, audit event              |
| webhook callback     | Repudiation / tampering              | authenticated source, replay protection, append-only log |

**Verification**: every entry point has at least one threat and concrete mitigation. Residual risks,
such as identity-provider outage, are recorded with an owner instead of silently accepted.

## Step 2: Run the mechanisms

From `learning/code/`, run the three local programs:

```text
python3 ex-22-23-passwords.py
python3 ex-34-jwt-integrity.py
python3 ex-25-signature.py
```

**Verification**: the correct password and original token are accepted; an incorrect password,
altered token, and altered signed message are rejected. These programs use generated or demo-only
values and do not expose a listener or access a network target.

## Step 3: Map OWASP 2025

| Category                             | Receipt-app status and prevention                              |
| ------------------------------------ | -------------------------------------------------------------- |
| A01 Broken Access Control            | present; check subject + action + receipt owner on every route |
| A02 Security Misconfiguration        | present; production disables debug and applies headers         |
| A03 Supply Chain Failures            | present; review lockfile, provenance, and advisories           |
| A04 Cryptographic Failures           | present; TLS and managed encryption/key access                 |
| A05 Injection                        | present; parameterized queries and structured process APIs     |
| A06 Insecure Design                  | present; STRIDE before feature approval                        |
| A07 Authentication Failures          | present; Argon2id, MFA policy, session rotation                |
| A08 Software/Data Integrity Failures | present; signed release artifacts and trusted CI               |
| A09 Logging & Alerting Failures      | present; protected audit events and response ownership         |
| A10 Exceptional Conditions           | present; bounded queues and safe generic failures              |

**Verification**: every category is addressed or explicitly justified N/A for the actual application.

## Step 4: Complete the secure-SDLC checklist

| Check                  | Status             | Evidence                                 |
| ---------------------- | ------------------ | ---------------------------------------- |
| Dependency review      | planned per change | lockfile diff + advisory disposition     |
| Secrets                | pass               | deployment injection; no source literals |
| Security headers       | pass               | automated response-header test           |
| Threat model           | pass               | Step 1 table reviewed with feature owner |
| Vulnerability response | planned            | owner, severity, target remediation date |

**Done bar**: the assessment has a threat for each boundary, a complete OWASP mapping, locally
runnable accept/reject evidence, and concrete secure-SDLC statuses. The next improvement is chosen
from residual risk, not from a generic tool output.
