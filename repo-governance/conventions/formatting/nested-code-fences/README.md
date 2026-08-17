---
title: "Nested Code Fence Convention"
description: "Standards for properly nesting code fences when documenting markdown structure within markdown content"
when_to_use: "Read this index to find the right Nested Code Fence Convention child document."
---

# Nested Code Fence Convention

- [Purpose, Scope, and the Orphaned Fence Problem](./01-purpose-scope-and-the-orphaned-fence-problem.md) — Defines what the Nested Code Fence Convention covers, the principles it implements, and how an orphaned closing fence breaks markdown rendering. Use when you need to understand why nested code fences need special handling or what this convention covers.
- [Fence Depth Rules and Complete Nesting Examples](./02-fence-depth-rules-and-complete-nesting-examples.md) — The 4-backtick-outer/3-backtick-inner depth rule with no orphaned fences, plus three complete worked examples of correctly nested fences. Use when writing a markdown example that itself contains a code block, and you need the correct fence depth pattern.
- [Common Mistakes and How to Fix Them](./03-common-mistakes-and-how-to-fix-them.md) — Three common nested-fence mistakes — extra closing fences, wrong fence depth, and mismatched fence pairs — each with a broken example and its fix. Use when a nested code fence example is rendering incorrectly and you need to diagnose which mistake caused it.
- [Validation Checklist and Troubleshooting](./04-validation-checklist-and-troubleshooting.md) — The pre-commit checklist for nested fences, plus symptom-diagnosis-solution troubleshooting for three common rendering failures. Use when a nested code fence example renders incorrectly and you need to diagnose and fix the symptom.
- [Testing, Integration, and Related Conventions](./05-testing-integration-and-related-conventions.md) — The process for testing nested fence rendering before committing, and how this convention integrates with related formatting conventions. Use when you need to verify a nested-fence example renders correctly or find related conventions that apply.
- [Examples in Documentation Types and References](./06-examples-in-documentation-types-and-references.md) — Worked nested-fence examples for tutorials, how-to guides, and reference docs, plus links to the CommonMark and GitHub Flavored Markdown fence specifications. Use when writing a nested-fence example in a tutorial, how-to guide, or reference document and want a template to follow.
