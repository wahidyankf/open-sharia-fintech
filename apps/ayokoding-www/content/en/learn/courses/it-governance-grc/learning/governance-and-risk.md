---
title: "Governance and risk scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

These first ten scenarios establish the decision chain: objective, risk, accountable owner,
treatment, and monitoring. Northstar Notes is fictional. Its founders, employees, customers, and
figures are constructed examples, not claims about a real service.

## Decision rights and risk framing

### Worked Scenario 1: Governance versus management

**Context**: Exercises co-01. Northstar's product lead wants the team to “make backups better”
after a customer asks how quickly notes could be restored.

**Decision artifact**:

| Decision layer | Northstar's statement                                                                                                                 |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------- |
| Governance     | “Customer workspace notes may lose no more than four hours of confirmed changes after a regional outage; the COO owns any exception.” |
| Management     | “The platform lead will select, test, and monitor a backup and restore process that can meet that objective.”                         |

**Verify**: the governance row sets an outcome, tolerance, and accountable business owner; the
management row chooses and operates a means. Neither row tries to do the other's job.

**Key takeaway**: Governance decides what reliable service means and who accepts the trade-off.
Management makes the service meet that direction.

**Why It Matters**: Calling every technical choice “governance” lets executives prescribe tooling
without owning the risk, while calling every risk tolerance “operations” leaves engineers to make
business trade-offs in private. Separating the two makes escalation possible before a customer
commitment silently becomes an engineering promise.

### Worked Scenario 2: COBIT domain map

**Context**: Exercises co-02. A board committee asks for evidence that leadership reviews material
technology risk. The GRC lead maps the work without claiming that a framework name performs it.

**Decision artifact**:

| Activity                    | Domain | Reason                                           |
| --------------------------- | ------ | ------------------------------------------------ |
| Approve the risk tolerance  | EDM    | Governing body evaluates, directs, and monitors. |
| Set the risk-review cadence | APO    | Management plans and organizes the program.      |
| Deploy monitoring           | DSS    | Operations delivers and supports the service.    |
| Review overdue remediation  | MEA    | Performance and conformance are measured.        |

**Verify**: each row is classified by the decision or operational purpose, and the table contains at
least one governance and one management activity.

**Key takeaway**: The domain map is a prompt for the right question, not a compliance label to paste
onto a meeting.

**Why It Matters**: A risk committee that also runs the operational backlog loses the independence
needed to challenge delivery. Conversely, an operations team cannot close a risk simply by working
hard on it. The map exposes a missing handoff between oversight, planning, delivery, and monitoring.

### Worked Scenario 3: Risk identification

**Context**: Exercises co-05 and co-07. Northstar introduces file attachments. The team writes risks
rather than a list of fears.

**Decision artifact**:

| ID   | Risk statement                                                                                                                   | Owner                 |
| ---- | -------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| R-01 | If a public attachment link is guessed, an unauthorized person could read a customer's note attachment, harming confidentiality. | Product security lead |
| R-02 | If attachment storage is unavailable, users could be unable to retrieve contractual records, harming availability.               | Platform lead         |
| R-03 | If malware is accepted as an attachment, a later downloader could be harmed, creating customer and operational impact.           | Engineering director  |

**Verify**: every row names an asset or objective, an event or threat, a consequence, and one owner.

**Key takeaway**: “Security risk” is not a usable risk statement; a decision needs the asset, event,
and consequence that make the trade-off concrete.

**Why It Matters**: Vague risks invite vague treatments like “improve security.” A named event and
consequence let different disciplines assess the same situation, determine who has authority to act,
and later test whether the selected control actually addresses the thing that could go wrong.

### Worked Scenario 4: Likelihood and impact

**Context**: Exercises co-06. Northstar uses a five-point scale, where 1 is rare or negligible and 5
is expected or severe. The team must compare R-01 with a low-impact branding error.

**Decision artifact**:

| Risk                           | Likelihood | Impact | Inherent score | Reason                                                                 |
| ------------------------------ | ---------: | -----: | -------------: | ---------------------------------------------------------------------- |
| Guessed public attachment link |          3 |      5 |             15 | Links may be shared or exposed; customer-content disclosure is severe. |
| Typo in help-center footer     |          4 |      1 |              4 | Likely to occur, but easy to correct with little customer harm.        |

**Verify**: the score equals the stated likelihood multiplied by impact, and the reasons explain the
numbers rather than treating the product as a fact.

**Key takeaway**: The score helps prioritize a conversation; it cannot replace the assumptions behind
the conversation.

**Why It Matters**: Teams often debate a single number as though it has scientific certainty. Writing
the scale and reasons makes a disagreement productive: challenge the exposure assumption or business
impact, then update the score when new evidence arrives instead of arguing about a color on a chart.

### Worked Scenario 5: Treatment choice

**Context**: Exercises co-08. The team evaluates three attachment decisions: public links, customer
managed storage, and unrestricted executable uploads.

**Decision artifact**:

| Risk                                  | Treatment | Decision and reasoning                                                                   |
| ------------------------------------- | --------- | ---------------------------------------------------------------------------------------- |
| Guessed link disclosure               | Mitigate  | Require authenticated, short-lived access and log downloads.                             |
| Customer wants its own storage region | Transfer  | Offer a contractually governed storage provider, retaining oversight of the integration. |
| Unrestricted executable uploads       | Avoid     | Do not accept executable formats in this feature.                                        |

**Verify**: each treatment is one of accept, mitigate, transfer, or avoid, and the decision explains
why it fits the stated risk. “Transfer” does not imply that Northstar has no residual responsibility.

**Key takeaway**: Treatment is a deliberate business choice; every choice leaves something to own.

**Why It Matters**: “Mitigate everything” wastes attention and creates controls that no one can
operate. Naming avoidance, transfer, and bounded acceptance lets leaders spend on the risks that
matter while keeping responsibility visible when an outside party or product decision carries part
of the exposure.

### Worked Scenario 6: A complete risk-register row

**Context**: Exercises co-07. The engineering director asks whether R-01 may stay open through the
next release.

**Decision artifact**:

| Field           | Entry                                                                                   |
| --------------- | --------------------------------------------------------------------------------------- |
| Risk            | R-01: guessed attachment link could disclose customer content.                          |
| Inherent rating | 15, using the documented 3 × 5 assessment.                                              |
| Treatment       | Mitigate with authenticated download authorization and an expiry of five minutes.       |
| Owner           | Product security lead.                                                                  |
| Residual rating | 6, pending an authorization review and download-log check.                              |
| Due and review  | Delivery by 2026-09-15; review monthly and after a link-related incident.               |
| Status          | Open; release requires the owner to approve a time-bounded exception if delivery slips. |

**Verify**: the row includes a risk, rating, treatment, accountable owner, residual rating, due date,
and review trigger.

**Key takeaway**: A register is not an inventory of worries. It is a queue of owned decisions.

**Why It Matters**: Without a due date and a review trigger, a risk becomes permanently “known” and
therefore effectively invisible. Without a residual rating, leaders cannot see whether a treatment
actually changed the exposure or merely produced an implementation task that feels reassuring.

### Worked Scenario 7: Policy, standard, procedure, and guideline

**Context**: Exercises co-16. Northstar's security lead finds an “access policy” that mixes executive
intent, a particular identity provider screen, and optional advice.

**Decision artifact**:

| Level     | Rewritten statement                                                                                    |
| --------- | ------------------------------------------------------------------------------------------------------ |
| Policy    | Access to customer content must be limited to authorized business need and reviewed.                   |
| Standard  | Privileged access must use phishing-resistant MFA and a separately approved account.                   |
| Procedure | The access administrator verifies approval, grants the role, records the ticket, and schedules review. |
| Guideline | Teams should prefer group-based roles to individual grants where practical.                            |

**Verify**: only the procedure contains mutable operational steps, and each level can change at a
cadence appropriate to its purpose.

**Key takeaway**: Stable intent belongs high in the hierarchy; detailed how-to belongs lower.

**Why It Matters**: When a vendor interface changes, a policy should not need executive reapproval.
When an engineer disputes whether access is required, a procedure alone cannot settle the obligation.
Separating levels keeps governance durable while allowing operations to improve without weakening the
underlying requirement.

### Worked Scenario 8: Control function

**Context**: Exercises co-17. The attachment team identifies three controls around malware uploads.

**Decision artifact**:

| Control                                                                       | Functional type | Why                                                    |
| ----------------------------------------------------------------------------- | --------------- | ------------------------------------------------------ |
| Reject disallowed file types before storage                                   | Preventive      | It blocks a class of harmful upload before acceptance. |
| Alert when a scan verdict is delayed                                          | Detective       | It reveals a condition requiring attention.            |
| Quarantine a file and invalidate its download links after a malicious verdict | Corrective      | It limits harm after the event has been identified.    |

**Verify**: the classification states when the control acts relative to the event, not whether it is
implemented in software or by a person.

**Key takeaway**: A complete control design often needs prevention, detection, and correction.

**Why It Matters**: A preventive control can fail; a detective control without a corrective action
only produces alerts; corrective action without detection begins too late. Naming the function
shows a gap in the chain and prevents a team from claiming that one familiar control solves every
stage of a risk.

### Worked Scenario 9: Control nature

**Context**: Exercises co-18. The same team classifies controls by implementation nature as well as
function.

**Decision artifact**:

| Control                                    | Nature         | Functional type |
| ------------------------------------------ | -------------- | --------------- |
| Access-review policy and manager approval  | Administrative | Preventive      |
| Signed download authorization              | Technical      | Preventive      |
| Locked media-disposal bin                  | Physical       | Preventive      |
| Quarterly review of failed-download alerts | Administrative | Detective       |

**Verify**: every row has one nature and one functional type; the two labels answer different
questions.

**Key takeaway**: “Technical” does not mean “preventive,” and a policy can be a real control when it
changes a governed decision.

**Why It Matters**: Control inventories become misleading when categories are treated as mutually
exclusive. The two-axis view makes it clear whether a risk depends entirely on technology, lacks
detection, or needs a human accountability mechanism alongside a technical mechanism.

### Worked Scenario 10: CSF current and target profile

**Context**: Exercises co-04. Northstar wants to describe its attachment-security posture to
leadership without claiming its framework profile is a certification.

**Decision artifact**:

| CSF Function | Current outcome                                    | Target outcome                                        | Gap owner             |
| ------------ | -------------------------------------------------- | ----------------------------------------------------- | --------------------- |
| Govern       | Risk owner exists but has no escalation threshold. | Risk appetite and exception path are approved.        | COO                   |
| Identify     | Attachment data flow is documented.                | Supplier and retention risks are also recorded.       | Product security lead |
| Protect      | Authenticated downloads exist.                     | Authorization is independently reviewed each quarter. | Engineering director  |
| Detect       | Download events are retained.                      | Unusual access has an investigated alert.             | Platform lead         |
| Respond      | Incident contacts are listed.                      | Attachment disclosure exercise is tested.             | Security lead         |
| Recover      | Backups exist.                                     | Restore time is measured against a business target.   | Platform lead         |

**Verify**: all six functions are either represented or deliberately out of scope with a reason, and
each gap has a named owner.

**Key takeaway**: A profile communicates a current-to-target decision; it is not a scorecard of
framework popularity.

**Why It Matters**: A long list of controls cannot tell leadership what should improve next. A
current and target profile turns broad framework language into a short set of owned outcomes, while
preserving the fact that risk management includes governance, response, and recovery as well as
preventive technology.

Next: [Compliance and controls scenarios](./compliance-and-controls).
