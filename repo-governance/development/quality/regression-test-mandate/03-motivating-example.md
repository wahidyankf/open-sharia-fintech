---
title: "Motivating Example"
description: "The bug batch that motivated this mandate."
category: explanation
subcategory: development
tags:
  - regression
  - testing
  - bug-fix
  - quality
  - gherkin
  - specs
created: 2026-06-22
when_to_use: "Use when you need the rationale behind this mandate."
---

# Motivating Example

The cost-of-living calculator work is the concrete case that motivated this mandate. Every bug
found during that work -- the savings tab ignoring the geographic filter, inputs not persisted
in the URL, a redundant UI panel, a hidden toggle that controlled visible output, a jargon label,
and a USD-only currency input -- was converted into a Gherkin scenario so it could not return.
Before that conversion, each bug was "fixed" but free to recur because no automated check
asserted the corrected behavior.

This mandate generalizes that practice into a standing rule: every bug found anywhere becomes
a pinned scenario that cannot be silently broken again.
