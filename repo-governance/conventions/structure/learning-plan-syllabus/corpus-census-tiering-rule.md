---
description: The REQUIRED at 99%/RECOMMENDED at 80% tiering rule derived from the section-frequency table, the capstone carve-out, and the method for reproducing the measurement.
when_to_use: Read this when applying or re-deriving the section tiers, or when checking whether a capstone-format file's missing sections are the known carve-out.
---

# Corpus Census: Tiering Rule and Reproduction

Part of the [Learning-Plan `syllabus/` Folder Convention](../learning-plan-syllabus.md), continuing
from the [Section Tiering Table](./corpus-census-section-tiering.md).

**Tiering rule**: REQUIRED at ≥ 99% of all 174 files; RECOMMENDED at ≥ 80%; OPTIONAL below that
threshold. The rule is stated, not just the resulting tiers, so a future author with a larger corpus
can re-derive the tiers by re-running the same per-file measurement rather than inheriting this frozen
list. The two REQUIRED-tier misses in the current corpus are the same file,
`syllabus/courses/capstone-forge-ready.md`, which carries neither `**Scope note**` nor
`## Concepts` — a legitimate capstone-format variant, not a defect, which is why a capstone MAY omit
these two REQUIRED sections without violating this convention.

**Reproducing these numbers**: for each corpus, iterate the `*.md` files under `syllabus/courses/`,
skipping `README.md` and `surgery.md`, and test each file for a section with
`grep -q '<pattern>' "$file"`. A recursive `grep -rl` over the whole directory instead
**silently includes `README.md` and `surgery.md`**, producing a wrong count — the per-file loop is
the reliable method.
