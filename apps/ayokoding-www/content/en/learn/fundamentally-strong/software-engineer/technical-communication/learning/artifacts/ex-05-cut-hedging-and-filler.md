---
title: "Artifact: Edited Paragraph — Event Bus Rationale"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 45
---

> Event-bus-replacement rationale, hedging and filler removed -- exercises co-14.

**Before** (76 words): So I think we're probably going to need to look at replacing our current queue
setup at some point, because it's honestly just kind of struggling to keep up, and I sort of feel
like we're basically going to hit a wall with it eventually if traffic keeps growing the way it has
been. I mean, it's not really broken yet, but I think it's worth maybe starting to look at
alternatives sort of soon.

**After** (34 words): Our current queue cannot sustain projected traffic growth. At current growth
rates, we hit its throughput ceiling within two quarters. We are evaluating alternatives now, before
that ceiling becomes an incident.
