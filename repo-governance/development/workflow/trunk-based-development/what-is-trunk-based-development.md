---
title: "What is Trunk Based Development?"
description: TBD's definition and its six core characteristics.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when explaining what TBD is or listing its core characteristics.
---

# What is Trunk Based Development?

**Trunk Based Development** is a source control branching model where developers work primarily on a single branch called the "trunk" (in Git, this is typically the `main` branch). Unlike feature-branch workflows, TBD minimizes long-lived branches and emphasizes frequent integration.

## Core Characteristics

1. **Single source of truth**: All work converges on one branch (`main`)
2. **Short-lived branches** (if any): Branches exist for < 1-2 days maximum
3. **Frequent commits**: Multiple commits per day to `main`
4. **Feature flags**: Hide incomplete work using toggles, not branches
5. **Continuous integration**: Every commit triggers automated testing
6. **Small changes**: Break work into tiny, mergeable increments
