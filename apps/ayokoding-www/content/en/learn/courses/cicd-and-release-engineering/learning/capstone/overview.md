---
title: "Capstone Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

This capstone models a small containerized service moving from a commit to a protected production
release. It joins matrix CI, a cache, a promotable artifact, environment approval, reusable local
automation, a typed canary decision, and simulated signature plus provenance verification.

## Run the delivery evidence

1. The CI workflow verifies two Python versions and uploads one deterministic artifact.
2. The deploy workflow names a protected production environment and never logs a token.
3. The local composite action factors rollout logic instead of duplicating it.
4. Run rollout.py with healthy and unhealthy signals to observe promotion and automatic rollback.

## Acceptance checks

- CI contains a matrix, cache, and artifact upload.
- The deploy workflow identifies production as its protected environment.
- A healthy, signed, attested candidate promotes; an unhealthy candidate rolls back.

**Key takeaway**: one immutable candidate should carry its evidence unchanged through every delivery
stage.

**Why it matters**: delivery safety comes from linked, inspectable evidence rather than a single
all-powerful deploy command. This local simulation lets a learner inspect the candidate digest, health
signal, approval boundary, and provenance check without using a registry, cloud account, or real
secret. A production pipeline should preserve the same proof while delegating the concrete deployment
to its chosen platform.
