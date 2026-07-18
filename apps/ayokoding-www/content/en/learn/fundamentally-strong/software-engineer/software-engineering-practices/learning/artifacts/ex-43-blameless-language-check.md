---
title: "Artifact: Rewriting a Postmortem into Blameless Language"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 83
---

> ex-43 &middot; exercises co-23 &middot; the same incident, named-individual language rewritten
> systemic.

**Draft (names an individual)**:

```text
Sam ran the stale ops-toggle script without checking its current state first, which re-disabled
gift-card redemption for 39 minutes. Sam should have verified the flag's state before running the
script.
```

**Rewritten, blameless**:

```text
The ops-toggle script re-disabled gift-card redemption for 39 minutes when it was run without a
pre-run state check. The script had no built-in guard against re-applying a change that was already
in effect, and no confirmation step surfaced the flag's current state before running -- both gaps
that any operator running this script, on any day, could equally have hit.

Fix: the script now prints the current flag state and requires an explicit confirmation before
applying a change (shipped same day). Longer term: audit other ops scripts for the same missing
guard.
```

**Verify**: the rewritten version contains zero sentences attributing the incident to a specific
person -- every sentence's subject is the script, the gap, or the fix, satisfying co-23's actor-
neutral rule.

**Key takeaway**: "Sam should have checked" blames a person for a gap the SYSTEM should have closed;
"the script had no guard" names the same gap as a fixable property of the tooling, which is also the
only version of the sentence that actually prevents a recurrence.

**Why It Matters**: blameless language is not about politeness for its own sake -- it changes what
the postmortem's fix section can even contain. "Sam should be more careful" produces no code change
and will happen again to whoever runs the script next; "the script had no confirmation guard"
produces the confirmation-prompt fix shown above, which protects EVERY future operator, including
Sam.
