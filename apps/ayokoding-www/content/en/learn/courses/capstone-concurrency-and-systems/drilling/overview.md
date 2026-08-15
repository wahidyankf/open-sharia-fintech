---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

Name the four golden signals: latency, traffic, errors, and saturation.

## Calculation practice

Compute an error-budget burn rate for a 99.9% monthly availability objective.

## Scenario judgment

The queue is full but error rate is low. Treat saturation as a user-impacting symptom before it becomes failure.

## Design exercise

Specify shutdown ordering for ingress, workers, queue drain, and metrics flush.

## Automaticity checklist

- [ ] I can set a bounded concurrency limit.
- [ ] I can attach an alert to an SLO rather than an internal event.
