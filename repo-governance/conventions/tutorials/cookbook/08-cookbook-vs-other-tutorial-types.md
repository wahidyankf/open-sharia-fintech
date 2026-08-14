---
title: "Cookbook vs Other Tutorial Types"
description: "Compares Cookbook against By-Example, How-To Guides, and By-Concept tutorial types to clarify when each applies."
when_to_use: "Read when deciding whether content should be a cookbook recipe, a by-example tutorial, a how-to guide, or a by-concept tutorial."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - cookbook
  - education
  - problem-solving
  - recipes
created: 2026-01-30
---

# Cookbook vs Other Tutorial Types

## Cookbook vs By-Example

| Aspect             | Cookbook                     | By-Example                           |
| ------------------ | ---------------------------- | ------------------------------------ |
| **Organization**   | By problem type              | Sequential (1-85)                    |
| **Reading order**  | Any order                    | Sequential recommended               |
| **Goal**           | Solve specific problem       | Learn language comprehensively       |
| **Coverage**       | Problem domains              | 95% language features                |
| **Code style**     | Copy-paste ready             | Educational with heavy annotations   |
| **Annotations**    | 0.5-1.5 per line (what)      | 1-2.25 per line (what + why)         |
| **Audience**       | Anyone with specific problem | Experienced devs switching languages |
| **Use case**       | "I need to parse CSV now"    | "I want to learn this language"      |
| **Self-contained** | Each recipe independent      | Examples build on each other         |

## Cookbook vs How-To Guides

| Aspect          | Cookbook (Tutorial)          | How-To Guide                        |
| --------------- | ---------------------------- | ----------------------------------- |
| **Nature**      | Learning-oriented            | Goal-oriented                       |
| **Scope**       | General problem + solution   | Specific task in specific context   |
| **Code**        | Complete, runnable example   | Steps to achieve goal               |
| **Location**    | `tutorials/cookbook/`        | `how-to/`                           |
| **Reusability** | Reusable pattern             | Specific to project/context         |
| **Explanation** | How solution works generally | Steps to achieve this specific goal |
| **Example**     | Recipe: Parse any CSV        | How to parse users.csv in this app  |

**Decision criteria**:

- **Cookbook recipe** if: General problem, reusable solution, educational value, applies across projects
- **How-to guide** if: Specific task, project-specific context, goal-oriented steps, one-time setup

## Cookbook vs By-Concept

| Aspect           | Cookbook              | By-Concept                         |
| ---------------- | --------------------- | ---------------------------------- |
| **Organization** | By problem type       | By concept hierarchy               |
| **Structure**    | Problem → Solution    | Concept → Examples → Exercises     |
| **Depth**        | Solve one problem     | Comprehensive concept coverage     |
| **Theory**       | Minimal (just enough) | Extensive (deep understanding)     |
| **Use case**     | "How do I solve X?"   | "I want to understand Y deeply"    |
| **Progression**  | No required order     | Beginner → Intermediate → Advanced |
