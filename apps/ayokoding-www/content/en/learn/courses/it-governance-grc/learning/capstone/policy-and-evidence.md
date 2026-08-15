---
title: "Capstone artifact: Policy and evidence plan"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

## Attachment protection policy

Northstar Notes protects customer attachments against unauthorized access, loss, and harmful
content through risk-based controls. Exceptions require an accountable owner, compensating controls,
an expiry, and a documented review. This policy is intentionally durable: it states the obligation,
not a vendor interface.

## Attachment protection standard

1. Customer attachment downloads require authenticated authorization, individual attribution, and a
   time-bounded grant.
2. Permitted uploads receive a documented verdict; suspicious content is quarantined and investigated.
3. Attachment restoration is exercised against approved business recovery targets.
4. High-tier attachment suppliers receive due diligence, reassessment, and an exit decision.
5. Control exceptions are approved, time-bounded, and reviewed before expiry.

## Operating procedure

The platform lead operates C-01 through C-03 and retains the resulting records. The product security
lead investigates C-05 exceptions. The operations lead operates C-04. The compliance lead reviews
the evidence package quarterly, records exceptions, and escalates material residual risk to the
Engineering director and COO according to the register.

## Evidence plan

| Control | Period and source                                      | Reviewer              | Exception rule                                  |
| ------- | ------------------------------------------------------ | --------------------- | ----------------------------------------------- |
| C-01    | Quarterly authorization sample and role-change records | Compliance lead       | Escalate unapproved or expired grants.          |
| C-02    | Monthly alert review and investigation tickets         | Product security lead | Escalate unresolved suspicious access.          |
| C-03    | Quarterly restore-exercise report                      | Engineering director  | Escalate any missed approved target.            |
| C-04    | Annual supplier assessment and contract-change log     | Compliance lead       | Escalate missing high-tier review or exit plan. |
| C-05    | Monthly verdict and quarantine record                  | Product security lead | Escalate unreviewed malicious-content event.    |

**Verify**: the policy states what must be true, the standard makes it testable, the procedure
names operators, and every evidence row identifies a control, period, source, reviewer, and
exception rule.

## Quarterly assurance summary

For the latest fictional period, C-01 and C-05 operated with recorded evidence; C-03 missed the
critical recovery target once. The Engineering director must recommend a remediation plan, and the
COO must decide whether the residual recovery risk remains within appetite. This is an assurance
decision, not a declaration of compliance or security.
