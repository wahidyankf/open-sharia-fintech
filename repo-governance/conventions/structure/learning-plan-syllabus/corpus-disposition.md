---
title: "Corpus Disposition"
description: The archive-with-plan versus promote-to disposition declaration every custodian plan carries in its selected technical form, the default rule, the promotion trigger test, and the corpus lifecycle diagram.
when_to_use: Read this when writing a custodian plan's Corpus Disposition section in its selected technical form, or when deciding whether a corpus should switch from archive-with-plan to promote-to.
category: explanation
subcategory: conventions
tags:
  - plans
  - syllabus
  - learning-bearing
  - custody
  - governance
created: 2026-07-22
---

# Corpus Disposition

Part of the [Learning-Plan `syllabus/` Folder Convention](../learning-plan-syllabus.md).

Every learning-bearing plan that **owns** a corpus (its **custodian** — see the
[Custody Rule](./custody-rule.md)) declares a `## Corpus Disposition` section in its selected
technical form: `tech-docs.md`, or a mapped companion owned by `tech-docs/README.md` when the
directory form is selected. The section has exactly one of the following values. A plan that only **consumes** another plan's
corpus never carries a `## Corpus Disposition` section — it is not learning-bearing in its own
right (see the [Learning-Bearing Trigger](./learning-bearing-trigger.md)'s negative example 2)
and instead carries the `custodied-by:<plan-id>` echo under its own `## Corpus Custody` heading,
defined in the Custody Rule.

| Value               | Meaning                                                                | Extra obligation                                                     |
| ------------------- | ---------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `archive-with-plan` | **Default.** The corpus moves to `plans/done/` with the plan folder    | None                                                                 |
| `promote-to:<path>` | The corpus has a consumer outside `plans/` and moves to a durable home | A delivery step performing the move and rewriting every inbound link |

```mermaid
%% Corpus lifecycle: the default path is the left spine; promotion is trigger-gated.
stateDiagram-v2
    [*] --> Authored: plan creates syllabus/
    Authored --> ArchiveWithPlan: no consumer outside plans/
    Authored --> Promoted: a non-plan consumer exists
    ArchiveWithPlan --> Archived: plan moves to plans/done/
    ArchiveWithPlan --> Promoted: non-plan consumer appears
    Promoted --> DurableHome: git mv + links rewritten
    Archived --> [*]
    DurableHome --> [*]
```

**The default is `archive-with-plan`.** A syllabus corpus is the specification a deliverable was
built from — the same role a hi-fi `.excalidraw.png` mockup plays for a UI screen — and, like that
mockup, it archives with the plan unless a concrete outside consumer exists. The durable product is
the shipped course body under `apps/ayokoding-www/content/`, not the syllabus that specified it.

**The promotion trigger is falsifiable, not a vibe.** A corpus MUST switch to `promote-to:` the
moment a **consumer outside `plans/`** reads it: a checker or agent, an Nx target, a build or
generation step, or shipped content front-matter that references a syllabus path. The test an author
applies is: **name the non-plan reader**. If none can be named, the disposition stays
`archive-with-plan`.
