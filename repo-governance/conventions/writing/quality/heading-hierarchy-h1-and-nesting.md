---
title: "Heading Hierarchy: Single H1 Rule and Nesting"
description: "The single-H1 rule and the requirement that headings not skip levels"
category: explanation
subcategory: conventions
tags:
  - content-quality
  - markdown
  - writing-standards
  - accessibility
  - documentation
created: 2025-12-07
when_to_use: "Read this when structuring a new document's headings or reviewing one for a heading-hierarchy violation."
---

# Heading Hierarchy: Single H1 Rule and Nesting

## Single H1 Rule

**Every markdown file MUST have exactly ONE H1 heading** - the document title.

PASS: **Correct (Single H1)**:

```markdown
# User Authentication Guide

## Overview

This guide covers authentication implementation.

## Setup

Follow these steps to set up authentication...
```

FAIL: **Incorrect (Multiple H1s)**:

```markdown
# User Authentication Guide

# Overview

This guide covers authentication implementation.

# Setup

Follow these steps...
```

**Why**: Single H1 provides clear document hierarchy for screen readers and SEO.

## Proper Heading Nesting

**Headings MUST follow semantic hierarchy** - don't skip levels.

PASS: **Correct Nesting**:

```markdown
# Document Title (H1)

## Section (H2)

## Subsection (H3)

#### Detail (H4)

## Another Section (H2)

## Another Subsection (H3)
```

FAIL: **Incorrect (Skipped Levels)**:

```markdown
# Document Title (H1)

## Subsection (H3) <!-- WRONG! Skipped H2 -->

##### Detail (H5) <!-- WRONG! Skipped H4 -->
```

**Why**: Proper nesting creates logical structure for screen readers and document outlines.
