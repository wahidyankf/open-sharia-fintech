---
title: "Commit Message Convention"
description: "Understanding Conventional Commits and why we use them in open-sharia-enterprise"
when_to_use: "Read this index to find the right Commit Message Convention child document."
---

# Commit Message Convention

- [Principles and Conventions Implemented](./principles-and-conventions-implemented.md) — The principles and companion conventions the commit message format respects. Use when tracing why the commit message convention exists back to the principles and conventions it respects.
- [What are Conventional Commits?](./what-are-conventional-commits.md) — What the Conventional Commits specification is and the overall header/body/footer structure it defines. Use when first learning what Conventional Commits is and why the project adopted it.
- [The Format Explained](./the-format-explained.md) — The header, body, and footer parts of a commit message and the rules for each. Use when writing a commit message and needing the exact rules for the header, body, or footer.
- [Valid Commit Types](./valid-commit-types.md) — The full table of commit types with examples, and a detailed description of what each type covers. Use when choosing which commit type (feat, fix, docs, etc.) applies to a change.
- [Scope Examples](./scope-examples.md) — Common scope names used across the project and example commit headers using them. Use when choosing a scope name for a commit.
- [Real-World Examples](./real-world-examples.md) — Worked good and bad commit message examples across common change types. Use when you need a concrete example commit message for a specific kind of change.
- [Why We Use This Convention](./why-we-use-this-convention.md) — The benefits Conventional Commits provides to developers, teams, the project, and users. Use when justifying why the project requires Conventional Commits.
- [How It's Enforced](./how-its-enforced.md) — The Commitlint tool, the Husky commit-msg hook that runs it, and the overall commit workflow. Use when understanding what automatically rejects a malformed commit message, and why.
- [Common Errors and Fixes](./common-errors-and-fixes.md) — The most common Commitlint rejection errors and how to fix each one. Use when a commit is rejected by Commitlint and you need to fix the specific error shown.
- [Best Practices](./best-practices.md) — Practical habits for clear descriptions, consistent scopes, single-purpose commits, useful bodies, issue references, and documenting breaking changes. Use when writing a commit message and want a habit-level checklist beyond the mechanical format rules.
- [Commit Granularity and When to Split Commits](./commit-granularity-and-when-to-split-commits.md) — Why splitting work into logical commits matters, and the five situations that call for separate commits. Use when deciding whether a set of changes should be split into multiple commits.
- [When to Combine Commits](./when-to-combine-commits.md) — The two cases where multiple files belong in one atomic commit — a single logical change, and tightly coupled changes. Use when deciding whether related changes across multiple files should land in one commit instead of several.
- [Commit Ordering Best Practices](./commit-ordering-best-practices.md) — How to order a sequence of related commits — create before update, refactor before fix, and a natural type progression. Use when a change requires multiple commits and you need to decide what order to make them in.
- [Atomic Commits](./atomic-commits.md) — What makes a commit atomic — self-contained, functional, single-purpose, and reversible — with a worked example. Use when checking whether a commit is atomic before finalizing it.
- [Commit Granularity: Real-World Examples](./commit-granularity-real-world-examples.md) — Three worked examples of splitting a feature, a refactor-and-fix, and a config change into properly granular commits. Use when you need a concrete example of correctly granular versus overly bundled commits.
- [Benefits of Proper Commit Granularity](./benefits-of-proper-commit-granularity.md) — How correct commit granularity helps code review, debugging, project history, and collaboration. Use when justifying why commit granularity discipline is worth the extra care.
- [Making Commits](./making-commits.md) — The three practical ways to make a commit — interactive one-liner, with a body flag, or multi-line in an editor. Use when you need the exact git commit invocation for a one-line, body-included, or multi-line commit message.
