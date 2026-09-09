---
description: New, follow-on, or changed direction reconciles against every open task-list item before any work responds to it
when_to_use: Use whenever the user supplies a new instruction, a follow-up, or a correction while a task list is already open.
---

# Standard 8: Reconcile the List When New Direction Arrives

When new, follow-on, or changed direction arrives while a task list is already open, the agent MUST
reconcile the list against it **before** taking any action on it. Reading it against every open item
comes first: some items are now wrong, some are superseded, some are unaffected, and the direction
usually implies more than one new item. Record that reconciliation, then continue.

This is not [Standard 4](./standards-1-to-5.md#standard-4--add-newly-discovered-tasks-as-they-surface).
Discovery is found by the agent and only ever **adds** to the list. Direction is given to the agent
and can **invalidate** items already on it. Only the second can make an open item wrong, which is why
appending the new work without re-reading the old is insufficient.

**Rationale**: Acting first and updating afterwards produces a list describing the task as it was
originally requested rather than as it is being performed — precisely the stale state
[Standard 2](./standards-1-to-5.md#standard-2--mark-in-progress-before-starting) and
[Standard 3](./standards-1-to-5.md#standard-3--mark-completed-immediately) exist to prevent, arriving
by a different route. The reconciliation is also the moment a contradiction between old and new
direction becomes visible. Carrying both forward silently resolves it by accident, and the resolution
is never recorded as the decision it was.

**What the reconciliation records**: which open items the direction invalidates, which it supersedes,
which it leaves untouched, and which new items it creates. An item the direction kills is closed with
that reason rather than left to be discovered later as apparently abandoned work.
