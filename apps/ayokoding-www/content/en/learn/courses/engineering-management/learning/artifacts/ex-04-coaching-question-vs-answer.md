---
title: "Artifact: Coaching Question vs Answer — Alex's Validation Design"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 44
---

> A directive answer versus a coaching question set for the same stuck design problem -- exercises
> co-04. Everline and every name here are fictional; every quote is an illustrative, constructed
> example.

**Directive version (what NOT to lead with)**: "Use a dead-letter queue -- synchronous validation
will add latency to the ingestion path and you don't want that on the hot path."

**Coaching version (what Priya actually sends)**:

1. What happens to an event today if it fails validation -- where does it go, and who notices?
2. If you delay the validation to a background process instead of the ingestion path itself, what
   does the ingestion path gain, and what does it lose?
3. Who's the audience for "an event failed validation" -- is it a human who needs to fix bad data,
   an alert that needs to fire immediately, or both?
