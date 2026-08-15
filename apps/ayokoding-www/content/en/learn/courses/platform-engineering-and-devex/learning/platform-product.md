---
title: "Platform product scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

This cluster establishes a platform only where it earns its place. Each artifact keeps the platform
team accountable for an internal product while keeping stream-aligned teams accountable for customer
outcomes.

## Diagnose before centralizing

### Worked Scenario 1: Platform before pain

_ex-01-platform-before-pain · exercises co-20_

**Context**: Harbor has 15 engineers, two services, and one shared deployment pipeline. Leadership
wants a dedicated platform team because peers have one.

**Decision artifact**:

| Observation                                                   | Decision                                                                              | Review trigger                                                              |
| ------------------------------------------------------------- | ------------------------------------------------------------------------------------- | --------------------------------------------------------------------------- |
| One-off setup work, no recurring queue, shared pipeline works | Do not form a dedicated platform team yet; keep a rotating enablement responsibility. | Reassess after repeated friction affects three teams or a delivery outcome. |

**Verify**: the decision names a measurable trigger rather than a fashionable title.

**Key takeaway**: A platform is an investment to amortize shared pain, not an organizational status
symbol.

**Why It Matters**: A small organization needs close product feedback more than an additional team
boundary. Creating a platform before recurring demand produces interfaces, roadmaps, and support
expectations without enough users to validate them. Recording the trigger preserves the option to
invest later while protecting current delivery capacity and customer focus. It avoids premature
bureaucracy.

### Worked Scenario 2: Cognitive-load audit

_ex-02-cognitive-load-audit · exercises co-05, co-01_

**Context**: Three Harbor teams each spend a day per release assembling the same deployment checks,
secret-request steps, and dashboard links.

**Decision artifact**:

| Repeated work                                       | Shared burden                                                     | Product hypothesis                                                                       |
| --------------------------------------------------- | ----------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Release checks, secret request, dashboard discovery | Each team learns and maintains the same non-differentiating flow. | A supported release capability reduces setup time without taking release ownership away. |

**Verify**: the candidate capability removes duplicated undifferentiated work and leaves the product
team responsible for its release decision.

**Key takeaway**: Reduce cognitive load by packaging repeated work, not by transferring ownership of
the product outcome.

**Why It Matters**: Cognitive load is finite. When every team repeatedly learns the same operational
glue, feature work slows and reliability knowledge fragments. The audit avoids centralizing
product-specific decisions: the platform standardizes the path and evidence, while the team still
chooses when and why to release for its users and customers in production.

### Worked Scenario 3: Platform-as-product framing

_ex-03-platform-as-product-framing · exercises co-01, co-02_

**Context**: An infrastructure group built a portal with no interviews and adoption is low.

**Decision artifact**:

| Product element | First version                                                          |
| --------------- | ---------------------------------------------------------------------- |
| Customer        | Stream-aligned teams creating new services                             |
| Problem         | First release requires handoffs across four queues                     |
| Outcome         | A team reaches a reviewable first release with fewer handoffs          |
| Feedback        | Monthly interviews, template completion rate, and escape-hatch reasons |

**Verify**: the roadmap begins with a customer problem and feedback loop, not a tool feature list.

**Key takeaway**: A portal becomes a platform product only when internal users can shape and judge it.

**Why It Matters**: Internal users can route around a poor experience, which makes adoption a useful
signal rather than disobedience. Treating a platform as a product creates discovery, support, and
iteration habits. It also prevents output theater, where a team celebrates a portal launch while
delivery teams still rely on chat messages and tickets.

### Worked Scenario 4: Team Topologies split

_ex-04-team-topologies-split · exercises co-03_

**Context**: Harbor's payment team owns customer outcomes but is also maintaining every cluster
add-on. A specialist cryptography component needs deep expertise.

**Decision artifact**:

| Concern                           | Team type             | Boundary                                    |
| --------------------------------- | --------------------- | ------------------------------------------- |
| Customer payment flow             | Stream-aligned        | Owns payment outcomes end to end.           |
| Shared delivery capability        | Platform              | Offers a supported self-service interface.  |
| Specialist cryptography engine    | Complicated subsystem | Owns exceptional expertise and a clear API. |
| Temporary cloud-practice coaching | Enabling              | Facilitates learning, then withdraws.       |

**Verify**: each team type is justified by the work it enables, rather than by seniority or reporting
line.

**Key takeaway**: Team boundaries should reduce dependencies and preserve fast customer-value flow.

**Why It Matters**: Calling every central group “platform” hides whether it is a gate, a support desk,
or a specialist subsystem. A purposeful split gives stream-aligned teams an outcome boundary,
platform teams a service boundary, and enabling teams a temporary teaching role. The distinction
makes support expectations and decision rights visible to everyone involved.

### Worked Scenario 5: Temporary collaboration

_ex-05-interaction-mode-collaboration · exercises co-04_

**Context**: Harbor is designing its first regulated-data service template with a pilot team; neither
side yet knows the right defaults.

**Decision artifact**:

| Interaction                                    | Time box   | Exit condition                                                                  |
| ---------------------------------------------- | ---------- | ------------------------------------------------------------------------------- |
| Collaboration between pilot and platform teams | Four weeks | Pilot validates defaults and the capability has a documented support interface. |

**Verify**: collaboration has a purpose, an end date, and a handoff condition.

**Key takeaway**: Collaboration is high-bandwidth discovery work, not a permanent dependency model.

**Why It Matters**: A new capability needs product context that a central team cannot invent alone.
Time-boxed co-design lets the platform learn from a real customer while preventing a private bespoke
solution from becoming permanent. Once the interface stabilizes, routine consumption should require
less coordination, leaving both teams capacity for their primary responsibilities.

### Worked Scenario 6: X-as-a-service

_ex-06-interaction-mode-xaas · exercises co-04_

**Context**: The template has been used by three teams, its inputs and support boundaries are stable,
and pilots no longer need weekly design sessions.

**Decision artifact**:

| Capability           | Consumer action                                      | Platform commitment                                       |
| -------------------- | ---------------------------------------------------- | --------------------------------------------------------- |
| Service starter path | Select documented inputs and use published defaults. | Maintain the interface, status signal, and change notice. |

**Verify**: consumption is possible through a documented interface without a standing meeting.

**Key takeaway**: Mature shared capabilities should shift from collaboration to X-as-a-service.

**Why It Matters**: Keeping a mature capability in collaboration mode turns every use into a
consulting engagement and limits scale. X-as-a-service is not abandonment: it requires a reliable
contract, support path, and deliberate evolution. The lower interaction cost is what frees the
platform to discover the next shared constraint across its customers efficiently.

### Worked Scenario 7: Platform team charter

_ex-07-platform-team-charter · exercises co-01, co-03_

**Context**: Harbor's platform group receives unrelated requests, from buying laptops to approving
production access, and cannot explain its purpose.

**Decision artifact**:

| Charter field | Statement                                                             |
| ------------- | --------------------------------------------------------------------- |
| Customer      | Harbor stream-aligned product teams                                   |
| Mission       | Reduce repeated delivery friction through self-service capabilities   |
| First product | Supported service-start path and database request                     |
| Exclusions    | Individual approvals, bespoke feature work, product release authority |
| Success       | Adoption, reduced wait time, safe outcomes, and customer feedback     |

**Verify**: the charter declares customers, a bounded product mission, exclusions, and outcome
measures.

**Key takeaway**: A charter turns a central group into an accountable product team.

**Why It Matters**: Without a charter, the platform becomes the place where all “shared” work goes,
including work that should remain with product or security owners. Explicit exclusions protect flow
and clarify escalation. Outcome measures also make it possible to retire a capability that does not
help its internal customers or solve a measurable problem.

### Worked Scenario 8: Platform versus ops silo

_ex-08-platform-vs-ops-silo · exercises co-01, co-06_

**Context**: The platform group requires a ticket and a three-day review before any team can use the
standard logging capability.

**Decision artifact**:

| Current step           | Replacement                                                      | Safety boundary                                                            |
| ---------------------- | ---------------------------------------------------------------- | -------------------------------------------------------------------------- |
| Manual approval ticket | Self-service request with standard retention and access defaults | Unusual retention or privileged access uses a documented exception review. |

**Verify**: the common safe case is ticket-free, while the exceptional case has a transparent path.

**Key takeaway**: A platform provides a paved road; an operations silo controls a queue.

**Why It Matters**: Manual review can feel safe because it makes someone visible, yet it often
creates delay without improving the common case. Encode repeatable safety decisions as defaults and
guard-rails, then reserve expert review for exceptions. This makes the secure path the easy path
rather than making teams choose between speed and compliance.
