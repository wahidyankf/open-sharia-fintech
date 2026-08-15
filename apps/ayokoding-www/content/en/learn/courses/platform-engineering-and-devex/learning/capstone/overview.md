---
title: "Capstone overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Create a coherent internal-platform slice for fictional Harbor: one golden path to a reviewable,
deployed service; one guard-railed self-service capability with an escape hatch; and a DevEx
measurement policy and dashboard brief. This is a no-code capstone. Describe the interfaces,
decisions, and evidence; do not create a portal, pipeline, script, or infrastructure resource.

The artifact set should make the common safe route easier than DIY while preserving product-team
ownership. A reviewer should be able to see what the capability does, who it serves, what it will
and will not do, how an unusual need is handled, and how the team will learn whether it helped.

## Concepts exercised

- [x] platform as a product for an internal customer (co-01, co-02)
- [x] cognitive-load reduction and appropriate maturity (co-05, co-20)
- [x] golden path, scaffolder, portal/catalog, and escape hatch (co-06 through co-10)
- [x] guard-railed ticket-free self-service and a platform contract (co-11 through co-13)
- [x] mechanism-versus-policy boundary (co-14)
- [x] DORA, SPACE, leading signals, and anti-weaponization (co-15 through co-18)
- [x] developer experience as the outcome to improve (co-19)

## Build order

1. Complete the [golden-path brief](./golden-path). It must state customer, outcome, defaults,
   ownership record, proof of a better-than-DIY experience, and an explicit off-path route.
2. Complete the [self-service contract](./self-service). It must turn one repeatable request into a
   ticket-free capability bounded by understandable guard-rails.
3. Complete the [DevEx measurement policy](./devex-metrics). It must define service-context signals,
   feedback questions, a review cadence, and prohibited uses.
4. Review all artifacts together. The catalog owner, customer, capability boundary, and measurement
   question must agree. If they do not, revise the product boundary rather than hiding the conflict.

## Acceptance criteria

- The golden path is demonstrably easier than its named DIY alternative and remains escapable.
- The self-service capability completes the common safe request without a ticket and explains how it
  blocks or escalates an unsafe or out-of-bound request.
- The platform contract identifies inputs, defaults, support expectation, ownership, limits, and an
  escape hatch.
- The measurement design uses DORA and SPACE in context, includes at least one leading signal, and
  explicitly forbids individual ranking, compensation, or discipline use.
- The artifacts frame Harbor's product teams as customers and preserve their product policy choices.

## Done bar

A product-team representative can choose the supported path, understand its limits, take a
legitimate exception route, and see how their feedback changes the platform. A platform lead can
explain the outcome being improved without claiming that a template, dashboard, or portal alone is
the product.

← Previous: [Metrics and DevEx scenarios](../metrics-and-devex) · Next:
[Drilling](../../drilling/overview) →
