---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Goal

Build a grounded QA application over a local corpus. It retrieves local chunks, returns cited structured
answers, validates a typed lookup tool, stops a bounded loop, and applies a deterministic injection guard.

## Run

Run `python3 code/app.py`. The capstone is fully offline and checks grounded citations, rejected invalid
tool arguments, a terminating loop, a latency/cost budget, and an injection-resistant context boundary.
