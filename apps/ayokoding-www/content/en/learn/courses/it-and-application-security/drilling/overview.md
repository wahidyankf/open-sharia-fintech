---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1.** What distinguishes authentication from authorization?

<details><summary>Answer</summary>

Authentication establishes an identity. Authorization decides whether that identity may take a
specific action on a specific resource. A successful login never proves the requested action is allowed.

</details>

**Q2.** Why is a parameterized query safer than manual escaping?

<details><summary>Answer</summary>

The driver sends the fixed SQL program and the supplied value separately, so the value cannot become
SQL syntax. Escaping is parser- and context-dependent guesswork.

</details>

## Calculation practice

An application generates a session ID from 16 random bytes. How many bits of entropy is that before
encoding, and how does it compare with the 64-bit session-entropy minimum?

<details><summary>Worked answer</summary>

Sixteen bytes contain 128 bits. That exceeds 64 bits, but the service still needs rotation, expiry,
secure cookie flags, server-side invalidation, and access checks.

</details>

## Scenario judgment

A reviewer finds a high-CVSS vulnerability in a library that appears only in an unused optional
integration. What should the team record before assigning a remediation target?

<details><summary>Reasoned answer</summary>

Confirm the exact locked version, deployment reachability, affected feature state, advisory
preconditions, asset exposure, and compensating controls. Then document an owner and time-bounded
decision; CVSS informs but does not complete local risk assessment.

</details>

## Design exercise

Create a STRIDE table for a document-sharing feature with browser upload, API, object storage, and a
notification worker. For every boundary, name one threat, mitigation, test, and residual-risk owner.
Then map the result to the relevant OWASP categories and decide which check belongs in CI.

## Automaticity checklist

- [ ] I can state which CIA property a control protects and name its trade-off.
- [ ] I can distinguish object authorization from authentication and check both.
- [ ] I can select hashing, encryption, or signatures from the required property.
- [ ] I can reject an untrusted JWT algorithm and explain token validation requirements.
- [ ] I can turn a scanner finding into an owned, evidence-based remediation decision.
