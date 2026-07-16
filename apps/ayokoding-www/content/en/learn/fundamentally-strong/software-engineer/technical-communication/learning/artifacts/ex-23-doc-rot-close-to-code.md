---
title: "Artifact: Relocated Design Doc — Notification Worker Architecture"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 63
---

> A drifted wiki design doc, moved close to the code and dated -- exercises co-17.

**Action**: delete the wiki page. Move its accurate remaining content (deployment topology, which has
not changed) into `services/notification-worker/docs/architecture.md`, dated at the top with today's
date, and rewrite the event-consumption section to describe the actual current Kafka-based design
(ADR-0005). Add a one-line pointer in `notification_worker/README.md`: "Full architecture: see
`docs/architecture.md`."

**Frontmatter added**: `Date: 2026-03-19` (last verified against the running code).
