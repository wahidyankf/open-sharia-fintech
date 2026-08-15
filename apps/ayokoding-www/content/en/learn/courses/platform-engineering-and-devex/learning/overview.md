---
title: "Learning overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Work through the 26 scenarios in order. They deliberately start with a question many organizations
skip: is there enough shared friction to justify a platform product? Harbor is fictional; its
platform team serves three stream-aligned product teams that repeatedly recreate service setup,
database requests, release checks, and ownership records.

## Platform product and organization design

- **co-01 · platform-as-product**: prioritize a platform capability from customer evidence, adoption,
  and outcomes, not executive mandate.
- **co-02 · internal-customer**: product teams are users whose context and feedback shape the offer.
- **co-03 · team-topologies**: platform, stream-aligned, enabling, and complicated-subsystem teams
  have different purposes.
- **co-04 · interaction-modes**: collaboration discovers; X-as-a-service consumes a stable offer;
  facilitating helps teams gain capability.
- **co-05 · cognitive-load**: remove accidental, repeated complexity without hiding product ownership.
- **co-20 · platform-maturity**: invest after measurable organization-wide friction, not fashion.

## Golden paths and self-service

- **co-06 · golden-path** and **co-07 · golden-path-escapable**: provide opinionated defaults that
  win on merit and a documented off-path route for legitimate needs.
- **co-08 · idp**, **co-09 · software-catalog**, and **co-10 · scaffolder-template**: a portal can
  expose ownership and templates, but it is a surface—not the platform itself.
- **co-11 · self-service**, **co-12 · guard-rails**, and **co-13 · platform-contract**: a useful
  capability is ticket-free within safe boundaries and explicit about support and exceptions.
- **co-14 · mechanism-vs-policy**: centralize reusable mechanisms and shared guard-rails; do not
  silently seize every product decision.

## Metrics and developer experience

- **co-15 · dora-metrics**: use the delivery performance measures in service context, including the
  current five-metric DORA model.
- **co-16 · space-framework**: include satisfaction, performance, activity, communication and
  collaboration, and efficiency and flow instead of claiming one number captures productivity.
- **co-17 · leading-vs-lagging**: use signals to ask useful improvement questions before outcomes
  arrive.
- **co-18 · metrics-anti-weaponization**: never rank people or set simplistic targets from system
  measures.
- **co-19 · devex**: make the developer's path to a safe outcome the product outcome to improve.

Every scenario contains an artifact and a verification rule. Those are the no-code equivalent of a
test: another person should be able to inspect the artifact and tell whether the decision is usable,
safe, bounded, and owned.
