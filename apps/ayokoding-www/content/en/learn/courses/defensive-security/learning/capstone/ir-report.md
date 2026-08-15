---
title: "Incident Report Template"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 2
---

# Synthetic Blue-Lab Incident Report

## Scope and evidence

- **Scope**: bundled `lab-events.ndjson` only; no production or customer telemetry.
- **Alert references**: `failed-login-burst`, `suspicious-request-evidence`.
- **Integrity note**: record the fixture revision used; do not invent observations not in the file.

## Detect and analyze

The fictional incident is scoped to four related events from the synthetic address `192.0.2.44`.
The two alerts are review prompts, not proof of identity or intent. Record the threshold, the one
benign event excluded by that threshold, and the uncertainty still remaining.

## Contain, eradicate, and recover

For the training service, contain by disabling the fictional affected account path; eradicate by
removing the deliberately unsafe training configuration; recover by restoring a known-good service
configuration and checking normal authentication. These are tabletop decisions only—no command on this
page operates a host.

## Lessons learned and hardening

- Add the reviewed detection to the local detection repository with its test fixture.
- Keep the lab's deny-by-default segment and disabled unused demo service.
- Re-run the fixture after any threshold or parser change.
- Assign an owner, due date, and verification evidence before closing the fictional incident.

## Current lifecycle note

NIST SP 800-61 Rev. 3 places incident-response considerations across CSF 2.0. The familiar sequence
above is retained as a clear tabletop checklist, not attributed as Rev. 3's standalone phase model.
