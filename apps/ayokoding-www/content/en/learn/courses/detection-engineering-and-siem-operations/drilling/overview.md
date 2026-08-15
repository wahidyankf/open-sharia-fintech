---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## 1. Recall: name the detection path

State the local path in order: raw event, decoder fields, base rule, correlation, dashboard evidence,
triage prompt, tuning decision. Explain the difference between an alert and a conclusion about intent.

## 2. Judgment: reduce noise without removing evidence

The fixture contains a single routine failed action and a repeated failed-then-success chain. Explain why
a threshold of one is noisy, why an unrestricted exception can become a blind spot, and what evidence
you need before changing the threshold.

## 3. Code: validate only local material

Run `sh ../learning/code/check-lab.sh`. Confirm the decoder XML, rules XML, dashboard plan, synthetic
fixtures, correlation result, and false-positive calculation pass. Do not substitute production logs or
add an endpoint argument; reproducibility is the exercise.

## 4. Transfer: write a tuning decision

Use the capstone [tuning record](../learning/capstone/tuning-record.md) to document a fictional rule
change. Include the prior and proposed threshold, retained true-positive fixture, expected false-positive
effect, reviewer, and a recheck date. Keep people, assets, and addresses invented.

## 5. Self-check: release a maintained hypothesis

Before enabling a specialist rule, ask: does the decoder extract the intended fields, does the rule have
both suspicious and benign tests, is its correlation scope explicit, does the dashboard show tuning
evidence, and does a responsible owner review it? A missing answer is work remaining, not a reason to
silence an alert.
