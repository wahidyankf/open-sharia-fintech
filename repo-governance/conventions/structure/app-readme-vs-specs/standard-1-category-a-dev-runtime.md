---
title: "Standard 1 — Content Split Rule: Category A (Dev-Runtime)"
description: The definition and content table for Category A — dev-runtime content that stays in an app or infra README.
when_to_use: Use when checking whether a piece of README content is dev-runtime (Category A) and should stay in the README.
category: explanation
subcategory: conventions
status: "Pilot — initial issue"
tags:
  - conventions
  - readme
  - specs
  - spec-tree-shape
  - pm-readability
  - c4
created: 2026-05-09
---

# Standard 1 — Content Split Rule: Category A (Dev-Runtime)

Each piece of content in an app or infra README belongs to exactly one of two categories. Apply these rules paragraph-by-paragraph when reviewing or trimming an existing README.

**Category A — Dev-runtime (stays in `apps/<app>/README.md` or `infra/*/README.md`)**

Content a developer needs to run, build, test, or lint THIS specific checkout on THEIR machine. It is intrinsically about the filesystem layout of the app folder and the Nx targets defined by its `project.json`.

| Content                                                    | Why it stays                                                                 |
| ---------------------------------------------------------- | ---------------------------------------------------------------------------- |
| One-paragraph "what is this" intro                         | Reader orientation                                                           |
| Status banner (pre-alpha, etc.)                            | Visible warning at app entry point                                           |
| Quick Start commands                                       | Setting up dev server is THIS-checkout-specific                              |
| Nx targets table (`nx dev`, `nx build`, `nx run X:test:Y`) | Targets are defined in `project.json` of THIS app                            |
| Environment variables consumed at runtime                  | Wire-level, depends on which env file the app reads                          |
| Project layout (top-level `src/`, `tests/`, configs)       | Filesystem of THIS checkout — top-level only, not per-context recursion      |
| Tech-stack version pinning                                 | "I'm running Node 24.13.1, Next.js 16, F# .NET 10" — version source-of-truth |
| One paragraph + link to `specs/` for behavior              | The pointer that completes the split                                         |
