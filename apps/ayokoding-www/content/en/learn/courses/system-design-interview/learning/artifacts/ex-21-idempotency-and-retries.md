---
title: "Artifact: 21 · idempotency-and-retries"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 60
---

> Constructed, vendor-independent interview exercise. **Concepts**: co-13, co-17.

## Prompt

Make a delivery attempt safe when a worker retries.

## Candidate artifact

Start by stating the assumption or question that constrains this decision. Give a concise answer
that a reviewer can trace from requirement to choice, then say the cost or uncertainty that remains.
This is a communication artifact, not a production architecture specification.

## Verify

Define an idempotency key and show why duplicate delivery does not double-apply.

## Debrief

A strong interview answer makes its reasoning inspectable: scope before detail, evidence before
preference, and a next question when the prompt leaves a material condition unknown.
