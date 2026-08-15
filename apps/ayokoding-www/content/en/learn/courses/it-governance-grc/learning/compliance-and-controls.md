---
title: "Compliance and controls scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

These scenarios take the risk decisions from the prior cluster and make them traceable to applicable
obligations, control outcomes, and evidence. They are fictional instructional artifacts, not legal,
audit, or certification advice.

## Framework scope and traceability

### Worked Scenario 11: ISO/IEC 27001 control theme

**Context**: Exercises co-03. Northstar groups a proposed control for contractor offboarding before
mapping it to a detailed control catalogue.

**Decision artifact**:

| Control statement                                                                                   | ISMS theme               | Reason                                                                                      |
| --------------------------------------------------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------------------------------- |
| Terminated contractor accounts are disabled within one business day, with monthly exception review. | People and technological | The obligation governs people lifecycle and is implemented through identity administration. |

**Verify**: the artifact names the risk being reduced (former contractor access), the accountable
owner, and a review cycle; it does not claim theme classification alone proves conformity.

**Key takeaway**: Framework mapping organizes a treatment; the risk and operating evidence make it
real.

**Why It Matters**: A team can map every control perfectly and still fail to disable a leaver's
account. Starting from the risk and owner avoids “control shopping,” where a catalogue entry is
chosen because it sounds familiar rather than because it changes the exposure that matters.

### Worked Scenario 12: Bidirectional control traceability

**Context**: Exercises co-19. A customer asks why download authorization must be reviewed quarterly.

**Decision artifact**:

| Risk                       | Control                                             | Framework outcome                           | Evidence                                                 | Owner                |
| -------------------------- | --------------------------------------------------- | ------------------------------------------- | -------------------------------------------------------- | -------------------- |
| R-01 attachment disclosure | C-04: authenticated, authorized, expiring downloads | NIST CSF Protect outcome for access control | Quarterly sampled authorization review and exception log | Engineering director |

**Reverse check**: C-04 maps only to R-01 today. If it is later claimed to reduce a new risk, the
register and evidence plan must be updated rather than silently broadening its purpose.

**Verify**: a reader can start at the risk and reach evidence, then start at the control and reach
its risk, owner, and framework outcome.

**Key takeaway**: Mapping is a graph, not a one-way spreadsheet export.

**Why It Matters**: One-way mappings hide two expensive failures: an important risk with no control,
and a control that consumes attention but has no agreed purpose. The reverse check makes those
orphans visible and gives an auditor or reviewer a short, reproducible path through the reasoning.

### Worked Scenario 13: SOC 2 criteria selection

**Context**: Exercises co-11. Northstar markets a collaborative note service and promises customers
that workspace content is protected and available, but it does not process customer payments.

**Decision artifact**:

| Criterion            | Include? | Service commitment or reason                                                            |
| -------------------- | -------- | --------------------------------------------------------------------------------------- |
| Security             | Yes      | Customers require protection from unauthorized access.                                  |
| Availability         | Yes      | Contractual uptime and restoration commitments apply.                                   |
| Confidentiality      | Yes      | Workspace notes are treated as confidential customer content.                           |
| Processing Integrity | Assess   | Include only if Northstar makes claims about complete and accurate processing outcomes. |
| Privacy              | Assess   | Include only if the service's personal-information commitments make it applicable.      |

**Verify**: every “Yes” traces to a real commitment, and every “Assess” has an explicit scoping
owner rather than being guessed from a sales objective.

**Key takeaway**: SOC 2 scope follows the system's commitments and handling, not a default package.

**Why It Matters**: Selecting every criterion can create irrelevant controls and a misleading
assurance story; selecting too few can omit the commitments customers rely on. The decision record
lets product, legal, security, and the assessor challenge scope before evidence collection makes a
bad assumption expensive.

### Worked Scenario 14: Card-data scope boundary

**Context**: Exercises co-12. Northstar wants subscriptions but sends users from its application to
a hosted payment page. The team documents the flow rather than declaring itself “out of scope.”

**Decision artifact**:

| Flow step                      | Card data present?                                                     | Decision                                                          |
| ------------------------------ | ---------------------------------------------------------------------- | ----------------------------------------------------------------- |
| Northstar subscription page    | No, it only creates a payment-session request.                         | Keep logs free of payment fields and review the integration.      |
| Hosted provider payment page   | Yes, handled by the provider.                                          | Contract and assess the provider relationship.                    |
| Provider callback to Northstar | No card number intended; payment status and customer reference arrive. | Validate and monitor the callback; test logs for accidental data. |

**Verify**: every handoff has a data classification and an owner; “not intended” is followed by a
control that tests or monitors the boundary.

**Key takeaway**: Reduced card-data exposure is a design claim that a documented flow must support.

**Why It Matters**: Teams often scope only the browser form and forget callbacks, support exports,
or logs. A data-flow record exposes these paths early, so an accidental storage decision becomes a
fixable engineering issue rather than a surprise discovered in an assessment or incident.

### Worked Scenario 15: Data-protection principles

**Context**: Exercises co-13 and co-27. A feature request proposes collecting a user's exact location
whenever they open Northstar Notes “for future analytics.”

**Decision artifact**:

| Question     | Decision                                                                                         |
| ------------ | ------------------------------------------------------------------------------------------------ |
| Purpose      | No current product function requires exact location.                                             |
| Minimization | Do not collect exact location. Use coarse region only if a documented localization need emerges. |
| Retention    | No new location record is retained.                                                              |
| Transparency | Update the notice before any future collection begins.                                           |
| Access       | Limit any future analytics dataset to the stated purpose and approved roles.                     |

**Verify**: every proposed field has a stated necessity and retention decision. “Useful someday” is
not treated as a purpose.

**Key takeaway**: Privacy by design removes unjustified data before it becomes a protection problem.

**Why It Matters**: Retrofitting deletion, notice, access, and breach analysis after data has spread
into logs and analytics costs far more than declining a speculative field at design time. The
artifact turns a broad principle into a reviewable engineering decision without pretending it
determines every jurisdiction's legal answer.

### Worked Scenario 16: Controller, processor, and incident escalation

**Context**: Exercises co-13. Northstar hosts notes for a customer, Alder Health, which determines
the purposes of processing. A cloud-storage supplier processes attachment objects for Northstar.

**Decision artifact**:

| Party            | Working role in this flow                                                                               | Operational duty                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Alder Health     | Controller for its workspace data                                                                       | Sets business purpose and instructions.                                   |
| Northstar        | Processor for Alder Health data; controller for its own account and billing data where it sets purposes | Maintains an incident escalation path and contractual assistance process. |
| Storage supplier | Subprocessor for attachment storage                                                                     | Notifies Northstar under the agreement and supports investigation.        |

**Escalation rule**: a suspected personal-data breach is immediately triaged and escalated to the
appropriate privacy and legal owners; they determine notification obligations and timing.

**Verify**: roles are assigned per processing activity, not per company globally, and the artifact
does not promise a notification outcome without the accountable legal decision.

**Key takeaway**: Role labels describe a specific purpose and means; they are not permanent company
badges.

**Why It Matters**: A provider may be a processor in one flow and a controller in another. Treating
the label as global causes missing contracts, unclear incident notices, and decisions made by people
who do not own the purpose. A per-flow record preserves the facts needed for qualified review.

### Worked Scenario 17: Healthcare safeguard coverage

**Context**: Exercises co-14. A healthcare customer uses Northstar for care-team notes containing
ePHI. The team makes a safeguard plan without claiming that a single safeguard satisfies every
requirement.

**Decision artifact**:

| Safeguard nature | Example decision                                                                      | Owner                |
| ---------------- | ------------------------------------------------------------------------------------- | -------------------- |
| Administrative   | Role-based access review and workforce training for support staff.                    | Compliance lead      |
| Physical         | Restrict physical access to support workstations and media handling areas.            | Operations lead      |
| Technical        | Strong authentication, least-privilege roles, audit logging, and encrypted transport. | Engineering director |

**Verify**: each relevant category has a concrete control and accountable owner; the plan identifies
where a customer agreement or specialist assessment is needed.

**Key takeaway**: Safeguards are complementary: people, premises, and systems all influence ePHI risk.

**Why It Matters**: A technically strong login cannot compensate for an untrained support process,
and a policy cannot recover an unencrypted exported file. The three-category view stops a program
from mistaking its most visible technical control for the whole protection model.

### Worked Scenario 18: Compliance versus security gap

**Context**: Exercises co-15. Northstar completed a required annual access review. Two weeks later,
an engineer discovers that a service account has a broadly shared secret with no expiry.

**Decision artifact**:

| Statement                          | Assessment                                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| “The annual review was completed.” | Compliance evidence for the defined review control.                                         |
| “The service account is safe.”     | Unsupported; the shared secret is a current security risk.                                  |
| Decision                           | Open R-12, rotate the secret, remove shared use, and add a review for non-human identities. |

**Verify**: the artifact preserves the completed evidence while recording the newly discovered
residual risk; it does not rewrite history or declare the program failed wholesale.

**Key takeaway**: Evidence of one control operating is valuable, but it never proves that every
current threat is controlled.

**Why It Matters**: If compliance and security are equated, teams either dismiss new risk because a
report is clean or treat all compliance evidence as meaningless after one gap. The disciplined move
keeps both truths: the review happened, and the security posture still needs a targeted correction.

### Worked Scenario 19: Policy-to-procedure chain

**Context**: Exercises co-16, co-17, and co-18. Northstar writes a narrow policy chain for privileged
production access.

**Decision artifact**:

| Layer     | Artifact                                                                                                                                                 |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Policy    | Privileged production access is granted only for approved business need and is reviewable.                                                               |
| Standard  | Privileged access uses individual accounts, MFA, time bounds, and logged elevation.                                                                      |
| Procedure | An approver records need and duration; an administrator grants a time-bounded role; the system records elevation; the reviewer checks exceptions weekly. |
| Evidence  | Approval ticket, role assignment record, elevation log, weekly exception review.                                                                         |

**Verify**: the evidence can demonstrate each mandatory standard boundary, and each procedure step
has an operational owner.

**Key takeaway**: A policy chain is complete only when intent can be operated and later evidenced.

**Why It Matters**: A policy with no operational path becomes a slogan; a detailed procedure with no
policy cannot answer why the friction exists. The chain ties executive direction to daily work and
gives reviewers something more reliable than a statement that “access is controlled.”

### Worked Scenario 20: Risk appetite and exception

**Context**: Exercises co-01 and co-08. A customer needs a legacy file format that cannot be scanned
by Northstar's current service. The product lead proposes a six-week exception.

**Decision artifact**:

| Field                      | Decision                                                                                      |
| -------------------------- | --------------------------------------------------------------------------------------------- |
| Risk                       | Malicious content could be stored and later downloaded.                                       |
| Proposed residual exposure | Higher than normal because automated scanning is absent.                                      |
| Compensating controls      | Isolated storage, download warning, manual review before release, and no public links.        |
| Accountable approver       | Engineering director, within the documented product risk appetite; otherwise escalate to COO. |
| Expiry and exit            | Expires 2026-10-01 or when scanner support is delivered, whichever is earlier.                |
| Monitoring                 | Weekly exception review and immediate escalation of a suspicious-file event.                  |

**Verify**: the exception has an accountable approver, explicit expiry, compensating controls, and a
route for a decision outside appetite.

**Key takeaway**: An exception is a time-bounded risk decision, not a permanent workaround with a
ticket number.

**Why It Matters**: Teams need a way to ship legitimate business work when a control is not yet
available. An exception mechanism preserves that flexibility while preventing temporary exposure
from becoming invisible technical debt that nobody is authorized to revisit.

Next: [Assurance and resilience scenarios](./assurance-and-resilience).
