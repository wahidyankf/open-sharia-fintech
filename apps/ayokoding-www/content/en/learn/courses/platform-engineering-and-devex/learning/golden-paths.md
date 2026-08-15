---
title: "Golden path scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

This cluster turns platform intent into usable, bounded capability. The path stays optional: a
platform earns adoption by making safe common work faster, while clear escape hatches prevent its
defaults from becoming a cage.

## Make the paved road compelling

### Worked Scenario 9: Golden-path CI wiring

_ex-09-golden-path-ci-wiring · exercises co-06, co-10_

**Context**: New Harbor services routinely omit a build check, container metadata, or deployment
readiness evidence because every team starts from an empty repository.

**Decision artifact**:

| Golden-path outcome         | Included default                                            | Team-owned choice                                   |
| --------------------------- | ----------------------------------------------------------- | --------------------------------------------------- |
| First release is reviewable | Standard build, container, deployment, and ownership checks | Product behavior, domain design, and release timing |

**Verify**: the path supplies the shared delivery wiring without claiming to decide the product's
architecture or release authorization in its own domain and context for customers and their needs.

**Key takeaway**: A golden path composes proven delivery practices into the easiest starting route.

**Why It Matters**: A template is useful when it removes setup uncertainty, not when it enforces an
unrelated architecture. Pre-wiring the repeatable CI, container, and deployment concerns lets a
team focus on its customer problem. Naming the remaining team-owned choices keeps the platform from
becoming a covert approval process. It also makes those product decisions visible and accountable
to the people closest to their consequences.

### Worked Scenario 10: Scaffolder adoption

_ex-10-scaffolder-adoption · exercises co-10_

**Context**: Service creation varies between teams and incident responders cannot reliably find an
owner, runbook, or delivery record.

**Decision artifact**:

| Template input                                      | Generated or registered outcome                                                                      |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| Service name, owner group, data class, runtime need | Catalog entry, ownership record, delivery-path selection, and links to required operational evidence |

**Verify**: the template requests only inputs needed for a clear outcome and creates a catalog record
that identifies an accountable owner.

**Key takeaway**: A scaffolder template makes the supported path repeatable and discoverable.

**Why It Matters**: Templates can either transfer a pile of hidden questions to a form or eliminate
the questions teams should not have to rediscover. A small set of meaningful inputs lets defaults do
the routine work. Recording ownership at creation reduces the common incident failure where everyone
can see the service but nobody knows who can decide.

### Worked Scenario 11: Golden-cage mandate

_ex-11-golden-cage-mandate · exercises co-07, co-06_

**Context**: Leadership proposes blocking every new repository unless it uses Harbor's first
template, even though it lacks a supported path for batch workloads.

**Decision artifact**:

| Request                           | Decision                                                                    | Follow-up                                                                 |
| --------------------------------- | --------------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Mandate template for all services | Decline; make the default opt-in and state its supported workload boundary. | Study batch-team needs and add a path only when a shared pattern emerges. |

**Verify**: the default is presented as the easiest supported option, with an explicit route outside
its documented boundary.

**Key takeaway**: A golden path is persuasive because it helps, not because it traps.

**Why It Matters**: A mandate hides product gaps by converting adoption into compliance. Teams with a
real outlying need will build unofficial workarounds, and the platform loses the feedback that would
improve it. An escape hatch makes exceptions visible, preserves autonomy, and gives the platform a
real demand signal for its next investment.

### Worked Scenario 12: Paved road worse than DIY

_ex-12-paved-road-worse-than-diy · exercises co-06_

**Context**: Teams avoid the service starter because it adds two days of review and creates a
repository they cannot easily adapt.

**Decision artifact**:

| Evidence                               | Diagnosis                                     | Improvement experiment                                                                         |
| -------------------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Most teams copy an old service instead | The paved road loses on time and flexibility. | Remove the common review, publish extension points, and compare time-to-first-review with DIY. |

**Verify**: the response fixes a measured friction rather than blaming users for low adoption.

**Key takeaway**: Adoption is evidence about the platform product, not a loyalty test.

**Why It Matters**: A path only reduces cognitive load when its costs are lower than rediscovery.
Treating workarounds as customer research reveals whether the problem is latency, missing capability,
or distrust. Measuring the revised path against the actual alternative keeps the platform team
honest about the outcome it claims to improve for users.

### Worked Scenario 13: Escape-hatch design

_ex-13-escape-hatch-design · exercises co-07, co-12_

**Context**: A team needs an unusual data store that the standard request cannot yet offer.

**Decision artifact**:

| Contract element | Escape-hatch rule                                                                    |
| ---------------- | ------------------------------------------------------------------------------------ |
| Trigger          | Need falls outside a published capability boundary.                                  |
| Request          | Team records rationale, owner, risk controls, and intended review date.              |
| Decision         | Named platform and relevant risk owners respond within a stated service expectation. |
| Learning         | Exception category is reviewed quarterly for a possible product improvement.         |

**Verify**: the exception has a predictable, owned process and produces learning rather than a
permanent private side path.

**Key takeaway**: An escape hatch is a designed interface for legitimate variation.

**Why It Matters**: “Ask us in chat” is neither autonomy nor governance. It makes exceptions depend
on social access and hides demand from the roadmap. A documented route provides a safe review for
unusual risk while showing whether enough teams share a need to justify an additional paved path later
for all customers.

## Make common work self-service and safe

### Worked Scenario 14: Self-service database request

_ex-14-self-service-db-request · exercises co-11, co-12_

**Context**: Every Harbor team opens a ticket for a small development database, creating a queue for
an otherwise standard, low-risk capability.

**Decision artifact**:

| Request class                     | Default outcome                                            | Guard-rail                                                                          |
| --------------------------------- | ---------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Development database within quota | Provision through the portal with an owner tag and expiry. | Size, network access, backup, and data-class limits are enforced before allocation. |

**Verify**: a safe request completes without a human ticket and an unsafe dimension is bounded before
the resource exists.

**Key takeaway**: Self-service converts an approved repeatable decision into a fast, safe capability.

**Why It Matters**: Tickets are appropriate when judgment is novel, but they are expensive machinery
for routine requests. Guard-railed self-service makes the compliant action quicker and supplies
consistent ownership metadata. The platform team can then improve defaults instead of repeatedly
replaying a decision that has already been made by every team many times.

### Worked Scenario 15: Guard-rail unsafe request

_ex-15-guard-rail-unsafe-request · exercises co-12_

**Context**: A developer requests a public, oversized database with production customer data and no
backup expectation through the self-service interface.

**Decision artifact**:

| Requested property                                        | Guard-rail response                                                | Safe next step                                                                              |
| --------------------------------------------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------- |
| Public access; excess size; sensitive data without backup | Reject the invalid combination and explain the failing boundaries. | Select a private approved profile, or use the documented exception route with a data owner. |

**Verify**: the response prevents the unsafe outcome, explains the boundary, and offers a legitimate
way forward.

**Key takeaway**: Guard-rails should guide a user to safety, not merely say no.

**Why It Matters**: An opaque denial shifts work into shadow infrastructure. Clear machine-enforced
boundaries make expectations learnable and consistent. They also distinguish routine safety policy
from a platform team's personal preference, which makes exceptions accountable and gives users a
path for needs that truly exceed the default profile safely and responsibly today.

### Worked Scenario 16: Platform contract

_ex-16-platform-contract-define · exercises co-13_

**Context**: Harbor's logging capability is widely used, but teams do not know its limits, support
hours, retention default, or how to request a deviation.

**Decision artifact**:

| Contract field       | Logging capability statement                                               |
| -------------------- | -------------------------------------------------------------------------- |
| Customer and input   | Product team sends structured service events with a catalog owner.         |
| Default and boundary | Approved retention and access profile; documented data-class restrictions. |
| Service expectation  | Status visibility, support channel, and change-notice practice.            |
| Escape hatch         | Retention or access exception with rationale and accountable data owner.   |

**Verify**: the contract states inputs, defaults, support expectation, limits, and an escape hatch.

**Key takeaway**: A platform contract makes a capability dependable without pretending it is limitless.

**Why It Matters**: Teams cannot make good architecture and risk decisions around an implied service.
An explicit contract makes trade-offs discussable before an incident and gives the platform a stable
interface to evolve. It also makes support load visible, which is necessary for treating the
capability as a product rather than an informal favor.

### Worked Scenario 17: Mechanism, not product policy

_ex-17-mechanism-not-policy · exercises co-14_

**Context**: Harbor's platform team proposes to require one programming framework for every service
because its template currently supports that framework best.

**Decision artifact**:

| Concern               | Platform mechanism                                                            | Product-team policy space                                                                      |
| --------------------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Safe service delivery | Provide supported build, ownership, observability, and deployment interfaces. | Select a framework that meets product needs within shared security and reliability boundaries. |

**Verify**: the platform standardizes a reusable delivery mechanism and does not turn a temporary
implementation preference into universal policy.

**Key takeaway**: Centralize shared mechanisms; leave contextual product decisions with the team.

**Why It Matters**: Some constraints genuinely need a common boundary, such as identity, data
handling, or operational evidence. Many technology choices do not. Confusing the two creates
unnecessary coupling and makes the platform responsible for product trade-offs it cannot know.
Mechanism-oriented design offers leverage while preserving team expertise and local ownership clearly
over time.

### Worked Scenario 18: IDP portal decision

_ex-18-idp-portal-decision · exercises co-08, co-09_

**Context**: Harbor asks whether to buy a portal, adopt an open portal, or write a custom front end.

**Decision artifact**:

| Need                         | Tool-agnostic decision criterion                                      |
| ---------------------------- | --------------------------------------------------------------------- |
| Discover services and owners | Catalog can represent ownership and useful operational links.         |
| Start common work            | Template or request surface supports the golden path.                 |
| Integrate safely             | Existing identity and delivery sources can supply authoritative data. |
| Sustain                      | Platform team can operate and evolve the chosen surface.              |

**Verify**: the decision is based on customer capabilities and operating cost, not portal branding.

**Key takeaway**: An internal developer portal is a self-service surface, not the platform strategy.

**Why It Matters**: A portal can expose a fragmented experience just as easily as it can unify one.
Choosing a representative tool such as Backstage does not replace product discovery, contracts, or
reliable source data. Starting from capability outcomes prevents a costly custom interface from
becoming the only visible result of platform engineering.

### Worked Scenario 19: Catalog ownership

_ex-19-catalog-ownership · exercises co-09_

**Context**: An incident affects a service called `invoice-events`, but responders cannot identify
the owner, data class, on-call route, or dependency status.

**Decision artifact**:

| Catalog field         | Entry                                                     |
| --------------------- | --------------------------------------------------------- |
| Service               | invoice-events                                            |
| Accountable owner     | Billing stream team                                       |
| Operational route     | Named on-call rotation and runbook link                   |
| Data and dependencies | Customer billing metadata; event broker and ledger API    |
| Lifecycle             | Production; review ownership quarterly and on team change |

**Verify**: a responder can find an accountable owner and operational context without a social
search.

**Key takeaway**: A catalog is valuable when it makes responsibility and context discoverable.

**Why It Matters**: Catalogs fail when they become stale inventories maintained for a portal. Tie
records to service creation, ownership changes, and operational review so the information has a
real user. Clear ownership also prevents the platform team from becoming the default owner of every
unknown service merely because it hosts the catalog.

### Worked Scenario 20: Internal-customer feedback

_ex-20-internal-customer-feedback · exercises co-02, co-01_

**Context**: Template adoption fell from eight teams to three, but the platform dashboard only shows
the count and the team has no explanation.

**Decision artifact**:

| Feedback prompt                               | Product action                                                                  |
| --------------------------------------------- | ------------------------------------------------------------------------------- |
| Where did the path take more effort than DIY? | Classify friction by wait, missing capability, confusing default, or trust gap. |
| Which users chose the escape hatch and why?   | Review exceptions with equal weight to supported-path feedback.                 |
| What outcome should improve?                  | Test one change against time-to-first-review and a short satisfaction question. |

**Verify**: the team talks to adopters and non-adopters, then commits to a falsifiable improvement.

**Key takeaway**: Internal customers are customers even when their usage is not revenue.

**Why It Matters**: Aggregate adoption tells a platform team that something changed, not why. Direct
feedback reveals the local context a dashboard cannot capture, especially for teams who avoid the
path. Treating escape-hatch users as evidence prevents survivorship bias and keeps roadmap choices
rooted in the experience the platform exists to improve each day.
