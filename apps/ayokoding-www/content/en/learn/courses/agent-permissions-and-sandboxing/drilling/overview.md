---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

What enforces tool permission: the model or the harness? Why is a production allow-list safer than a training harness with broad permissions?

## Scenario Judgment

Classify a request to read a repository file, send data to an unknown host, and delete a directory as allow, ask, or deny; explain the policy evidence for each.

## Hands-on Implementation

Write a pure function that maps a tool request and policy to `deny`, `ask`, or `allow`, then test that untrusted prompt text cannot change the result.

## Automaticity Checklist

- [ ] I distinguish model intent from harness authority.
- [ ] I can explain filesystem, network, and process sandbox boundaries.
- [ ] I can identify train-vs-production permission asymmetry as risk.

## Extension challenge

For a file-writing tool, specify the allowed paths, approval boundary, execution sandbox, and the
audit record that makes a denied action explainable.
