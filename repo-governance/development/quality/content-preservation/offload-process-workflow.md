---
title: "Offload Process Workflow"
description: "The step-by-step workflow for performing an offload."
category: explanation
subcategory: development
tags:
  - content-preservation
  - condensation
  - offload
  - zero-loss
  - documentation
created: 2025-12-14
when_to_use: "Use when executing a content offload end to end."
---

# Offload Process Workflow

Follow this systematic process when offloading content:

## Step 1: Identify Content to Condense

- Read the file completely
- Identify verbose sections with detailed explanations
- Look for duplicated content across files
- Check if content is unique or already in conventions

## Step 2: Determine Offload Destination

- Is this a new convention? → Option A
- Expands existing convention? → Option B
- Shared across multiple files? → Option C
- Development practice? → Option D

## Step 3: Create or Update Convention Document

- Use `docs-maker` for new files
- Use `Edit` tool for updating existing
- Move ALL relevant content (be comprehensive)
- Add examples, rationale, anti-patterns
- Update frontmatter (`updated` date)

## Step 4: Replace Original Content

- Write 2-5 line summary
- Add link to convention doc
- Remove verbose details
- Maintain readability and context

## Step 5: Update Index Files

- Add new conventions to `repo-governance/conventions/README.md`
- Add new development docs to `repo-governance/development/README.md`
- Maintain alphabetical ordering

## Step 6: Verify All Cross-References

- Use Glob to verify convention doc exists
- Test all links point to correct files
- Verify links include `.md` extension
- Check bidirectional references where appropriate

## Step 7: Confirm Zero Content Loss

- Read original content
- Read convention doc
- Verify all information preserved
- Confirm no unique details lost
- Document any intentional omissions

## Step 8: Update Related Files

- Search for references to condensed topic
- Update other files to link to convention
- Eliminate duplication across repository
- Maintain consistent terminology
