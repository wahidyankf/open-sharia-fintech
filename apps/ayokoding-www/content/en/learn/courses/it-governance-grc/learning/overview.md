---
title: "Learning overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This course teaches GRC through decision artifacts, not a framework memorization contest. Work
through the scenarios in order: each later artifact assumes that a risk has an objective, an owner,
and an explicit decision. The fictional **Northstar Notes** service used below stores customer
workspace notes and has a small engineering team, a product owner, and external service providers.

## Governance and risk

### co-01 · Governance versus management

Governance evaluates options, directs priorities, and monitors outcomes. Management plans, builds,
runs, and measures the work needed to carry out that direction. **Verify**: a governing decision
states the outcome and risk tolerance; a management action states how work will be performed.

### co-02 · COBIT as a decision map

COBIT groups governance and management objectives into EDM, APO, BAI, DSS, and MEA. Use it to ask
whether a decision belongs to oversight, planning, change, operations, or measurement. **Verify**:
a classification names the activity's purpose, not only the team that performs it.

### co-03 · ISMS

An information security management system connects policy, risk treatment, controls, and continual
improvement. ISO/IEC 27001 is a framework for this system, not a checklist that makes a system safe.
**Verify**: the proposed control has a risk, owner, and review cycle.

### co-04 · NIST CSF outcomes

NIST CSF 2.0 frames cybersecurity outcomes through Govern, Identify, Protect, Detect, Respond, and
Recover. The functions are concurrent, not a linear project plan. **Verify**: a profile distinguishes
the current outcome from a targeted outcome and explains the gap.

### co-05 · Risk lifecycle

Risk work identifies uncertainty, analyzes likelihood and impact, chooses treatment, then monitors
whether the treatment remains effective. **Verify**: a risk statement names an asset or objective,
a threat or event, and a consequence.

### co-06 · Risk assessment

Qualitative scoring makes assumptions visible; it does not turn uncertain judgment into arithmetic
truth. A likelihood-times-impact score helps compare risks only when the scale definitions are
consistent. **Verify**: every score cites the stated scale and is reviewed after material change.

### co-07 · Risk register

A risk register records a decision-ready view: statement, inherent rating, owner, treatment,
residual rating, due date, and status. **Verify**: no open material risk lacks an accountable owner
or a next review date.

### co-08 · Risk treatment and appetite

Accept, mitigate, transfer, or avoid are choices; each leaves a residual risk. Risk appetite is the
boundary that tells an owner which residual risks need escalation. **Verify**: an acceptance names
the accountable role, expiry, and reason it is within appetite.

### co-09 · Integrated GRC

Governance chooses direction, risk informs trade-offs, and compliance supplies applicable
obligations and evidence. Treating them as one traceable system avoids duplicate assessments.
**Verify**: a control maps to both a risk and an obligation or stated business objective.

### co-10 · Three Lines

The first line owns and manages risk, the second line supports and monitors, and the third line
provides independent assurance. The governing body oversees all three. **Verify**: an auditor does
not own the control they later evaluate.

## Compliance and control design

### co-11 · SOC 2 criteria

SOC 2 engagements use Trust Services Criteria: Security plus, as applicable, Availability,
Processing Integrity, Confidentiality, and Privacy. Selecting criteria is a scoping decision, not a
marketing preference. **Verify**: every selected criterion is tied to a service commitment or data
handling claim.

### co-12 · PCI DSS scope

Cardholder-data exposure drives PCI DSS scope; reducing the systems that store, process, or transmit
that data can reduce the assessment boundary, but only if the flow supports the claim. **Verify**:
the data-flow inventory includes every handoff and service provider.

### co-13 · Privacy obligations

Data-protection work begins with purpose, necessity, and roles. A controller determines purposes
and means; a processor acts for a controller. **Verify**: a data inventory states purpose, category,
retention, recipient, and owner before a privacy claim is made.

### co-14 · Healthcare safeguards

For regulated health data, administrative, physical, and technical safeguards are complementary.
Classify safeguards by the capability they provide, not by the department that paid for them.
**Verify**: every ePHI scenario includes safeguards across the relevant categories and an owner.

### co-15 · Compliance is not security

Compliance can establish a baseline or contractual assurance; security asks whether current threats
and business consequences are actually reduced. Passing an assessment never eliminates risk.
**Verify**: an assurance report lists material residual risks rather than declaring the system safe.

### co-16 · Policy hierarchy

Policy states durable intent, standards state mandatory boundaries, procedures describe repeatable
steps, and guidelines offer advice. **Verify**: a policy does not bury tool-specific steps that must
change more often than the policy itself.

### co-17 · Control function

Preventive controls try to stop an event, detective controls reveal it, and corrective controls
restore or limit harm afterward. One control may support more than one outcome. **Verify**: the
classification says when the control acts relative to the event.

### co-18 · Control nature

Administrative, technical, and physical controls describe how a control is implemented. They are a
different axis from preventive, detective, and corrective. **Verify**: a classification can state
one functional type and one nature without contradiction.

### co-19 · Control traceability

A defensible mapping works both ways: from a risk to its treatment and controls, and from a control
to its owner, evidence, framework outcome, and risks. **Verify**: an orphan control or unmapped
risk is visible rather than silently excluded.

## Assurance, resilience, and improvement

### co-20 · Audit and evidence

Internal audit provides independent assurance inside the organization; an external auditor reports
under the scope of an engagement. Evidence must be timely, attributable, complete enough to test,
and preserved. **Verify**: an evidence item identifies the control, period, source, reviewer, and
exceptions.

### co-21 · Business continuity and disaster recovery

Business continuity keeps essential work operating; disaster recovery restores technology after a
disruption. RTO is the target recovery time, and RPO is the tolerable data-loss interval. **Verify**:
each target is tied to a business process and tested, not guessed from infrastructure capacity.

### co-22 · Third-party risk

Suppliers extend the organization's risk boundary. Assess the service, data, dependency, and exit
plan rather than relying only on a vendor badge or questionnaire. **Verify**: a high-tier supplier
has an owner, reassessment cadence, and contingency decision.

### co-23 · Security awareness

Training changes behavior only when it is relevant, role-based, reinforced, and measured through
safe indicators. Completion alone is weak evidence of capability. **Verify**: a program has a
specific audience, behavior goal, and improvement action for poor results.

### co-24 · Maturity and accountability

Maturity measures whether a process is ad hoc, repeatable, managed, or improving; RACI makes the
decision rights explicit. A mature-looking spreadsheet cannot compensate for shared accountability.
**Verify**: every RACI activity has one accountable person.

### co-25 · Assurance roll-up

Assurance rolls operational signals, control testing, exceptions, and accepted risks into a decision
for leadership. A green dashboard without exceptions is not assurance. **Verify**: a report names
its data period, material exceptions, trend, owner, and requested decision.

### co-26 · Software licensing and IP risk

Dependency governance considers license obligations, provenance, approved use, and components in
the delivered product. An SBOM supports discovery but does not decide compatibility by itself.
**Verify**: an exception names the component, license, distribution model, owner, and expiry.

### co-27 · Privacy by design

Privacy by design makes data minimization, purpose limitation, access boundaries, and retention
choices early design constraints rather than a release checklist. **Verify**: a design can explain
why each personal-data field is necessary and when it is deleted.

Next: [Governance and risk scenarios](./governance-and-risk.md).
