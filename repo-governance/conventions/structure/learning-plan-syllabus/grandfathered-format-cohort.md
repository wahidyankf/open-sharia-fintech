---
description: The 17-file ordered-list divergence inside plan 02's corpus, why it is identified as a separate authoring cohort, and why bullets are canonical for new course files while this cohort is not retrofitted.
when_to_use: Read this when you find a course file using an ordered list for co-NN/ex-NN entries and need to know whether it is a known, accepted divergence or a new defect.
---

# Grandfathered Format Cohort

Part of the [Learning-Plan `syllabus/` Folder Convention](../learning-plan-syllabus.md).

The measured corpus shows a two-marker authoring-cohort split inside plan 02's 120 course files: a
majority cohort of 97 files renders its `co-NN`/`ex-NN` concept and exercise lists as bullets
(`- **co-01 …`), while a divergent cohort of exactly **17 files** renders the same lists as an ordered
list (`1. **co-01 …`) and, in every one of those 17 files, also omits the `**Short summary**` line.
That coincidence is what identifies the 17 as a separate authoring cohort rather than 17 independent
typos.

Bullets are canonical: the repo-wide markdownlint configuration pins unordered list style to `dash`
(the `MD004` setting), and both plan 06 and plan 07 use bullets uniformly (54 of 54 files). New course
files MUST use bullets. The existing 17-file ordered-list cohort inside plan 02 is **grandfathered** —
retrofitting it is explicitly out of scope for this convention, so it is named here as a known,
accepted divergence rather than silently tolerated or mistaken for a defect discovered later.
