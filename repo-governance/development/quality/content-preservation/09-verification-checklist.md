---
title: "Verification Checklist"
description: "The checklist to verify an offload preserved all content."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use after performing an offload, to verify nothing was lost."
---

# Verification Checklist

Before completing a content offload, verify:

## Content Preservation

- [ ] All unique content moved to convention doc
- [ ] No valuable information deleted
- [ ] Examples preserved or improved
- [ ] Rationale and context maintained
- [ ] Anti-patterns documented

## Convention Document Quality

- [ ] Convention doc is comprehensive
- [ ] Frontmatter complete and accurate
- [ ] Updated date reflects changes
- [ ] Structure follows convention patterns (see [Convention Writing Convention](../../../conventions/writing/conventions.md))
- [ ] Examples include PASS: good and FAIL: bad

## Original File Updates

- [ ] Replaced with 2-5 line summary
- [ ] Link to convention doc included
- [ ] Link uses correct relative path
- [ ] Link includes `.md` extension
- [ ] Summary maintains context

## Index and Navigation

- [ ] Convention indexed in README.md
- [ ] Alphabetical ordering maintained
- [ ] Category correct (conventions vs development)
- [ ] No broken links introduced

## Cross-Reference Integrity

- [ ] All links verified with Glob
- [ ] Link targets exist
- [ ] Relative paths correct
- [ ] Bidirectional references maintained

## Zero Content Loss

- [ ] Read original content completely
- [ ] Read convention doc completely
- [ ] Verified all information present
- [ ] No unique details lost
- [ ] Document any intentional omissions

## Consistency Across Repository

- [ ] Same terminology used everywhere
- [ ] No contradictions introduced
- [ ] Duplication eliminated
- [ ] Single source of truth established

## Correct Folder Choice

- [ ] Content offloaded to appropriate folder (conventions/ or development/)
- [ ] Content/format standards → conventions/
- [ ] Process/workflow standards → development/

**Verify Correct Folder Choice:**

**For repo-governance/conventions/** (content/format):

- File naming, linking, emoji, diagrams, colors
- Content quality, mathematical notation
- Tutorials, acceptance criteria
- Documentation organization

**For repo-governance/development/** (process/workflow):

- AI agent standards
- Commit messages, git workflow
- Code review, testing, release processes
- CI/CD, deployment strategies

**Red Flags:**

- Testing strategy in conventions/ (should be development/)
- File naming in development/ (should be conventions/)
- Git workflow in conventions/ (should be development/)
- Diagram format in development/ (should be conventions/)
