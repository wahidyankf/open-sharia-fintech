---
title: "Metrics and DevEx scenarios"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

This cluster measures the delivery system and the experience of the people using it. Metrics create
questions for improvement; they do not establish a ranking of people or a target to game. The current
DORA guidance describes five service-level delivery measures and warns against disparate comparisons
and competing with the numbers. [DORA delivery metrics guide](https://dora.dev/guides/dora-metrics/)

## Measure a system, not people

### Worked Scenario 21: DORA baseline

_ex-21-dora-baseline · exercises co-15_

**Context**: Harbor has opinions about slow delivery but no shared baseline for one service.

**Decision artifact**:

| Service-level measure           | Baseline question                                             |
| ------------------------------- | ------------------------------------------------------------- |
| Change lead time                | How long does a committed change take to reach production?    |
| Deployment frequency            | How often does this service deploy in its operating context?  |
| Failed deployment recovery time | How quickly is a deployment failure restored?                 |
| Change fail rate                | What share of deployments needs immediate intervention?       |
| Deployment rework rate          | What share is unplanned work following a production incident? |

**Verify**: each measure is scoped to an identifiable service and the record includes period, source,
and an improvement question.

**Key takeaway**: DORA establishes a contextual delivery baseline, not a universal leaderboard.

**Why It Matters**: Starting with one service keeps data collection and interpretation close to the
actual delivery system. The current DORA guidance evolved from four keys to a five-metric model, so
the artifact records the measure definitions instead of repeating a slogan. A baseline lets Harbor
test whether platform work changes flow and stability over time.

### Worked Scenario 22: SPACE beyond DORA

_ex-22-space-beyond-dora · exercises co-16_

**Context**: Harbor's delivery numbers improve after a new template, yet developers report that
discovering the right path and getting help is exhausting.

**Decision artifact**:

| SPACE dimension                 | Complementary signal                                   |
| ------------------------------- | ------------------------------------------------------ |
| Satisfaction and well-being     | Short recurring question about confidence and friction |
| Performance                     | Service delivery outcome in context                    |
| Activity                        | Template or self-service use, interpreted cautiously   |
| Communication and collaboration | Number and quality of necessary handoffs               |
| Efficiency and flow             | Time from intent to a reviewable safe outcome          |

**Verify**: the review uses more than one dimension and states what a signal cannot prove by itself.

**Key takeaway**: Developer productivity and DevEx are multidimensional, so one activity count is
not a verdict.

**Why It Matters**: Faster deployments can coexist with confusing documentation, interrupted work,
or an exclusionary support model. SPACE supplies questions that expose those dimensions without
pretending to calculate a person's worth. Combining qualitative feedback with delivery evidence
helps a platform team improve the path people actually travel rather than optimizing the easiest
number to collect.

### Worked Scenario 23: Leading-signal choice

_ex-23-leading-signal-choice · exercises co-17_

**Context**: Harbor only sees quarterly lead-time results, long after users abandon the starter path
or wait on an exception.

**Decision artifact**:

| Desired outcome           | Leading signal                                      | Review question                                            |
| ------------------------- | --------------------------------------------------- | ---------------------------------------------------------- |
| Faster first safe release | Time to complete the common starter path            | Which step creates the longest wait or rework?             |
| Fewer unsafe workarounds  | Escape-hatch reason and guard-rail failure category | Is a common need missing from the supported path?          |
| Better confidence         | Short post-use confidence response                  | What documentation or support gap explains a low response? |

**Verify**: each leading signal is connected to a plausible action and is not presented as proof of
the eventual outcome.

**Key takeaway**: Leading signals help teams intervene before lagging outcomes make a problem plain.

**Why It Matters**: A lagging metric such as quarterly recovery performance matters, but it cannot
tell a platform team what to change today. A useful leading signal is close enough to a decision to
guide an experiment. Naming both the outcome and the question prevents teams from collecting proxy
data merely because it is available.

### Worked Scenario 24: Metrics as stack rank

_ex-24-metrics-as-stack-rank · exercises co-18_

**Context**: An executive asks to rank engineers by deployment frequency and use the result in
performance reviews.

**Decision artifact**:

| Proposed use                                   | Decision                                                                               | Safe alternative                                                                                          |
| ---------------------------------------------- | -------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Individual stack ranking from delivery numbers | Refuse. The measures describe a socio-technical service system, not individual output. | Review service trends with the teams, alongside context and qualitative feedback, to select improvements. |

**Verify**: the policy expressly forbids individual ranking, compensation, or discipline use of the
dashboard.

**Key takeaway**: Delivery metrics are for system learning, never employee surveillance.

**Why It Matters**: A deployment reflects product scope, review practices, release controls, shared
services, and many contributors. Assigning it to one person breaks the system model and encourages
harmful behavior such as unnecessary changes or avoiding difficult work. The anti-weaponization
boundary protects the honesty of the data and the people needed to improve it.

### Worked Scenario 25: Goodhart target

_ex-25-goodhart-target · exercises co-18_

**Context**: Harbor sets “deploy every day” as a personal target. Engineers split harmless changes
and defer riskier fixes to protect their number.

**Decision artifact**:

| Observed behavior                                 | Diagnosis                                                    | Reset                                                                                                    |
| ------------------------------------------------- | ------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| Artificially small changes and deferred hard work | The measure became the target and lost its diagnostic value. | Remove the individual target; inspect service flow, change quality, recovery, and user outcome together. |

**Verify**: the reset changes the incentive and asks an outcome-oriented question rather than setting
a replacement quota.

**Key takeaway**: When a signal becomes a target, it becomes easier to optimize than the outcome.

**Why It Matters**: Goodhart's law is a warning about governance, not an excuse to avoid measurement.
Teams still need evidence about flow and reliability, but must be free to reveal a difficult system
constraint. Restoring the metric as a conversation starter makes gaming unnecessary and returns
attention to safe customer value instead of visible personal activity.

### Worked Scenario 26: DevEx friction survey

_ex-26-devex-friction-survey · exercises co-19_

**Context**: Leadership asks whether developer experience is “good,” but has only an adoption chart
for the portal.

**Decision artifact**:

| Question                                          | Companion evidence                               | Use                                           |
| ------------------------------------------------- | ------------------------------------------------ | --------------------------------------------- |
| Can you complete the common path with confidence? | Starter-path duration and support-contact themes | Identify usability or documentation friction. |
| Where do you lose flow?                           | Wait and handoff categories                      | Prioritize a bottleneck experiment.           |
| Would you choose this path again? Why or why not? | Adoption and escape-hatch reasons                | Test whether the path wins on merit.          |

**Verify**: responses are aggregated and protected from individual attribution, and each result has a
published follow-up action or explanation.

**Key takeaway**: DevEx combines reported experience with operational signals and visible
improvement.

**Why It Matters**: A portal visit does not prove a developer reached a safe outcome or felt able to
act independently. Short, respectful surveys supply context that instrumentation cannot see, while
delivery signals prevent anecdotes from becoming the whole story. Closing the loop—sharing what
changed or why it did not—builds the trust that makes future feedback useful.

## Measurement guardrail

Use the dashboard only for learning at service, team, or value-stream level. DORA explicitly warns
that context varies and that competing with the metrics is counterproductive. The platform team's
job is to make constraints visible and improve the system with its customers—not to create a
scoreboard. [DORA delivery metrics guide](https://dora.dev/guides/dora-metrics/)
