---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

IT Governance, Risk, and Compliance (GRC) is how an organization turns security work into an
owned decision, a proportionate control, and evidence that the control actually operated. It is not
paperwork layered on top of engineering. It is the traceability that lets a team answer: what could
go wrong, who decided what level of risk is acceptable, what reduces that risk, and what proves it?

This is a leadership **no-code** Annotated-concept course. Every company, person, system, control,
and decision artifact is fictional and constructed for learning. There is no runnable software and
no `code/` directory. You will work through 30 decision scenarios, from a single risk-register row
to an auditable assurance roll-up for a small service.

## Prerequisites

- **Prior topic**: [IT and Application Security](/en/learn/courses/it-and-application-security).
  That course explains technical controls and security operations; this course explains how an
  organization assigns risk ownership, selects control outcomes, and turns operational evidence into
  assurance.
- **Tools and environment**: a plain-text or spreadsheet workflow is sufficient. The deliverables
  are decision records, matrices, policies, and evidence plans rather than programs.
- **Assumed knowledge**: the CIA triad, basic threat modeling, and a practical understanding that a
  technical control may fail, be bypassed, or be irrelevant to a particular risk.

## Scope boundary

This course governs and assures technical work; it does not replace
[IT and Application Security](/en/learn/courses/it-and-application-security), which teaches the
engineering mechanisms themselves. It also does not prepare a reader to provide legal advice,
certify an organization, or independently issue an audit opinion. Laws, contracts, and framework
requirements apply differently by jurisdiction, customer, and system: involve qualified counsel,
assessors, and accountable business owners when a real decision depends on them.

## The mental model

Use the chain below for every scenario in this course:

1. State the objective and the risk to it.
2. Name the accountable risk owner and the decision they must make.
3. Choose a treatment and controls that are proportionate to the risk.
4. Map each control to a relevant framework outcome only after the risk is clear.
5. Retain timely, reviewable evidence and use it to report residual risk.

A framework is a vocabulary and a set of outcomes, not a substitute for judgment. NIST describes
CSF 2.0 as a non-prescriptive taxonomy of cybersecurity outcomes; its six Functions are Govern,
Identify, Protect, Detect, Respond, and Recover. [NIST CSF 2.0](https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20)
COBIT distinguishes the governing body's Evaluate, Direct, and Monitor activities from management's
delivery work, and its core model contains 40 governance and management objectives. [ISACA COBIT 2019](https://www.isaca.org/store2/product/CB19FGM)

## Why this exists

Controls often accumulate because a questionnaire asked for them, a customer complained, or an
incident frightened someone. That approach can produce many artifacts but no assurance: a control
without a named risk may be irrelevant, a risk without an owner cannot be accepted responsibly, and
an implemented control without evidence cannot be relied upon. GRC makes the decisions and the
evidence visible enough to challenge, improve, and defend.

The course progresses in three clusters: governance and risk decisions, control and compliance
mapping, then assurance, resilience, and organization-level reporting. Each scenario includes a
concrete artifact, a checkable verification rule, a takeaway, and the reason the decision matters.

## Primary-source reading

- [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework) — outcomes and profiles
  for communicating cybersecurity risk.
- [ISO/IEC 27001:2022](https://www.iso.org/standard/27001) — the ISMS standard; consult the licensed
  text and a qualified assessor for requirements and applicability.
- [AICPA Trust Services Criteria](https://www.aicpa-cima.com/resources/download/2017-trust-services-criteria-with-revised-points-of-focus-2022)
  — the Security, Availability, Processing Integrity, Confidentiality, and Privacy criteria used in
  SOC 2 engagements.
- [GDPR text on EUR-Lex](https://eur-lex.europa.eu/eli/reg/2016/679/oj) — primary legal text for
  Article 5 principles and Article 33 notification; seek jurisdiction-specific advice.
- [IIA Three Lines Model](https://www.theiia.org/globalassets/site/about-us/about-the-profession/three-lines-model-updated.pdf)
  — a model for governance, management, and independent assurance roles.

## How verification works

No scenario asks you to run a command. Instead, every artifact has an observable test: a risk row
has an owner and treatment; a control mapping traces in both directions; a RACI row has exactly one
accountable person; evidence can be tied to a period and a control. Read the artifact and test that
property. That is the appropriate no-code analogue to a test passing.
