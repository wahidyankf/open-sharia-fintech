---
title: "Choosing the Right Tutorial Type"
description: A decision tree and quick-reference table for picking the correct tutorial type based on prior experience and learning goal.
when_to_use: Use when you are unsure which of the six tutorial types fits a piece of content you are about to write.
category: explanation
subcategory: conventions
tags:
  - conventions
  - tutorials
  - naming
  - learning-paths
created: 2025-12-03
---

# Choosing the Right Tutorial Type

## Decision Tree

```mermaid
%% Color palette: Blue #0173B2, Orange #DE8F05, Teal #029E73, Purple #CC78BC, Brown #CA9161, Gray #808080
graph TB
 START[Need to learn a topic?] --> Q1{Never used before?}
 Q1 -- Yes --> Q2{Quick 5-min check?}
 Q1 -- No --> CB[Cookbook]

 Q2 -- Yes --> IS[Initial Setup]
 Q2 -- No --> Q3{Experienced dev?}

 Q3 -- Yes --> BE[By Example]
 Q3 -- No --> Q4{Enough to explore?}

 Q4 -- Yes --> QS[Quick Start]
 Q4 -- No --> Q5{Full foundation?}

 Q5 -- Yes --> BEG[Beginner]
 Q5 -- No --> Q6{Production systems?}

 Q6 -- Yes --> INT[Intermediate]
 Q6 -- No --> Q7{Expert mastery?}

 Q7 -- Yes --> ADV[Advanced]
 Q7 -- No --> CB

 style IS fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style QS fill:#DE8F05,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style BEG fill:#029E73,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style INT fill:#CC78BC,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style ADV fill:#CA9161,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style CB fill:#808080,stroke:#000000,color:#FFFFFF,stroke-width:2px
 style BE fill:#0173B2,stroke:#000000,color:#FFFFFF,stroke-width:2px
```

## Quick Reference Table

| Tutorial Component            | Coverage  | Purpose                               |
| ----------------------------- | --------- | ------------------------------------- |
| **FULL SET TUTORIAL PACKAGE** | **0-95%** | **All 5 components for completeness** |
| ↳ Foundational                |           |                                       |
| Initial Setup                 | 0-5%      | Installation and verification         |
| Quick Start                   | 5-30%     | Core concepts for exploration         |
| ↳ Learning Tracks             |           |                                       |
| By-Example (3 files)          | 95%       | **PRIORITY:** Code-first, move fast   |
| By-Concept (3 files)          | 95%       | Narrative-driven, learn deep          |
| ↳ Practical Reference         |           |                                       |
| Cookbook                      | Practical | Problem-solving recipes               |
