---
title: "Retired Single-File Structure"
description: Records the prospective boundary for existing plans created under the retired single-file exception.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when reviewing an existing single-file plan against the prospective transition rule.
---

# Retired Single-File Structure

New formal plans never use the retired all-in-one `README.md` exception. Use the fixed core in
[Structure Decision](./structure-decision.md).

Do not migrate or report structure findings against:

- immutable plans in `plans/done/`;
- the Rhino plan already in progress when the current mature-plan contract landed; or
- another existing plan whose creation predates that contract.

When such a plan is otherwise edited or executed, preserve its recorded structure. New material
within it must remain internally consistent and safe, but the edit does not silently convert the
plan to the current document set.
