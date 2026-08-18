---
title: "Tutorial Structure Requirements: Required Sections (Items 3-4)"
description: "Specifies the required prerequisites section and the learning-objectives section that follow a tutorial's introduction."
when_to_use: "Read when drafting the prerequisites section or the learning-objectives section of a tutorial."
category: explanation
subcategory: conventions
tags:
  - tutorials
  - diataxis
  - learning
  - pedagogy
  - documentation
  - teaching
created: 2025-12-03
---

# Tutorial Structure Requirements: Required Sections (Items 3-4)

## 3. Prerequisites

**Purpose**: Set clear expectations for required prior knowledge

**Required Elements**: - List of prerequisite knowledge - Links to prerequisite tutorials (if available) - Assessment checklist (learner can self-verify readiness)

**Format**:

```markdown
## Prerequisites

Before starting this tutorial, you should:

- [Prerequisite 1 with clear description]
- [Prerequisite 2 with clear description]
- [Prerequisite 3 with clear description]

**Optional but helpful:**

- [Nice-to-have knowledge 1]
- [Nice-to-have knowledge 2]

If you're new to [topic], start with [link to beginner tutorial].
```

**Rules**: - Be specific about what "knowing" means - Distinguish required vs optional prerequisites - Provide paths for learners who lack prerequisites - Use checkboxes () for self-assessment

## 4. Learning Objectives

**Purpose**: Clear, measurable outcomes the learner will achieve

**Required Elements**: - 3-7 specific learning objectives - Written in measurable terms (Bloom's taxonomy verbs) - Focused on learner achievements (not content coverage)

**Format**:

```markdown
## Learning Objectives

By the end of this tutorial, you will be able to:

1. **[Verb] [Object]** - [Brief context or application]
2. **[Verb] [Object]** - [Brief context or application]
3. **[Verb] [Object]** - [Brief context or application]
```

**Bloom's Taxonomy Verbs** (by cognitive level): - **Remember**: Define, list, recall, identify - **Understand**: Explain, describe, summarize, interpret - **Apply**: Calculate, demonstrate, solve, use - **Analyze**: Compare, contrast, differentiate, examine - **Evaluate**: Assess, judge, critique, justify - **Create**: Design, develop, construct, formulate

**Good Example**:

```markdown
1. **Calculate** the weighted average cost of capital (WACC) for a company
2. **Explain** why WACC is used as the discount rate in NPV analysis
3. **Apply** WACC to evaluate investment decisions
```

**Bad Example** (not measurable):

```markdown
1. Understand WACC
2. Learn about cost of capital
3. Know financial formulas
```
