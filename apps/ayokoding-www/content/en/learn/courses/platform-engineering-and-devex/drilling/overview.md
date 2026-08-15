---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Use this sequence to turn the course concepts into decisions you can inspect. All prompts concern
fictional organizations. For a real platform, include the affected customers and accountable risk,
security, and product owners.

## Recall Q&A

**Q1 (co-01, co-02).** What makes a platform a product rather than a mandate?

<details>
<summary>Answer</summary>

It has identified internal customers, a recurring problem, an explicit capability boundary,
feedback, and outcome measures. Adoption and escape-hatch use are product evidence, not compliance
scores.

</details>

**Q2 (co-03, co-04).** When should collaboration become X-as-a-service?

<details>
<summary>Answer</summary>

Use collaboration to discover a new capability with a time box and exit condition. Shift to
X-as-a-service when inputs, defaults, support, and change expectations are stable enough for a team
to consume the capability without ongoing co-design.

</details>

**Q3 (co-06, co-07).** What proves a golden path is not a golden cage?

<details>
<summary>Answer</summary>

The default path is easier than DIY for its supported use case, its limits are visible, and a
documented escape hatch handles legitimate needs outside those limits. The path earns adoption on
merit rather than blocking alternatives.

</details>

**Q4 (co-11 through co-13).** What belongs in a self-service platform contract?

<details>
<summary>Answer</summary>

State the customer and input, safe defaults, guard-rails and boundaries, ownership, support or
change expectation, non-goals, and the escape hatch. The common safe case should be ticket-free.

</details>

**Q5 (co-15 through co-18).** Why is DORA unsuitable for individual ranking?

<details>
<summary>Answer</summary>

Delivery measures describe a service system involving scope, collaboration, tooling, review,
operations, and many people. Ranking individuals discards context, encourages gaming, and destroys
the candid data needed to improve the system.

</details>

## Scenario judgment

Three teams independently request the same observability setup, but each has a different product
policy and alert threshold. The platform lead proposes one mandatory alert configuration.

<details>
<summary>Reasoned answer</summary>

Create a self-service observability mechanism with common ownership, routing, and safe baseline
capabilities. Do not mandate product-specific alert policy if it is not a shared safety boundary.
Interview the teams, publish a contract and defaults, and retain an escape hatch. Measure whether the
capability reduces setup handoffs and improves confidence rather than measuring compliance with one
configuration.

</details>

## Design exercise

For a fictional organization with four product teams, create a one-page platform-product brief:

1. Name a repeated cognitive-load problem and the internal customers affected.
2. Define one golden path, its defaults, and the product decisions it deliberately leaves to teams.
3. Define one ticket-free self-service request, its guard-rails, and an escape-hatch record.
4. Add two DORA measures, two SPACE-informed signals, one leading signal, and a question each will
   help answer.
5. Write one sentence that prohibits individual ranking or performance use of the information.

Review the brief using the capstone acceptance criteria. A reader should be able to distinguish an
internal product from an operations queue and a learning system from a scorecard.

## Automaticity checklist

- [ ] I can decide whether repeated organizational friction justifies a platform investment.
- [ ] I can distinguish platform, stream-aligned, enabling, and complicated-subsystem purposes.
- [ ] I can choose collaboration, X-as-a-service, or facilitating deliberately and time-box discovery.
- [ ] I can make a golden path easier and escapable rather than mandatory.
- [ ] I can write a platform contract with defaults, boundaries, support, and an escape hatch.
- [ ] I can separate a reusable mechanism from a contextual product policy.
- [ ] I can interpret DORA and SPACE as complementary system-learning inputs.
- [ ] I can protect metrics from Goodhart effects and individual weaponization.
