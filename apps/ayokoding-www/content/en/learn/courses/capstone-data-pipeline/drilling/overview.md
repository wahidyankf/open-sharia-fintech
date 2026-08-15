---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

Why preserve bronze? It supports replay, lineage, and reconciliation.

## Calculation practice

Reconcile source rows, accepted rows, rejected rows, and gold aggregates for one batch.

## Scenario judgment

A question has no supporting gold row. Return uncertainty rather than a plausible answer.

## Design exercise

Draw lineage from raw batch through quality gate and serving query to cited answer.

## Automaticity checklist

- [ ] I can make a pipeline idempotent.
- [ ] I can distinguish data quality from answer quality.
