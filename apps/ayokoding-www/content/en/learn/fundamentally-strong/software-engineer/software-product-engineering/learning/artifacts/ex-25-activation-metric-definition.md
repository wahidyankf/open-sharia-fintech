---
title: "Artifact: Activation Metric Definition — Kestrel"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 65
---

> A precise activation-event definition for Kestrel -- exercises co-20. Kestrel is a fictional
> product; every quoted number, question, or finding here is an illustrative, constructed example,
> not real data or a real transcript.

**Activation event**: a new team's manager publishes their first complete weekly schedule -- every
open shift for the coming week assigned to a specific staff member -- within 3 days of signing up.

**Why this and not "created an account" or "added one employee"**: creating an account or adding a
single employee record costs the manager almost nothing and delivers no value on its own --
neither event corresponds to Kestrel actually replacing the manager's prior paper-and-texts
process for even a single week.

**Measurement**: the signup timestamp and the first-schedule-published timestamp for every team,
published to the analytics pipeline as `days_to_first_publish`; a team "activates" if that value is
≤ 3 days.
