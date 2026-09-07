---
description: The definition and content table for Category B content that moves to specs/, plus the three-question test for classifying a README paragraph.
when_to_use: Use when checking whether a piece of README content is behaviour/architecture (Category B) and must move to specs/, or when applying the split-rule decision test.
---

# Standard 1 — Content Split Rule: Category B, and Applying the Rule

**Category B — Behaviour, contract, or architecture (moves to `specs/apps/<app-family>/`)**

Content that describes WHAT the system does — what URLs it exposes, what user flows exist, what API endpoints, what bounded contexts, what design decisions, what integration points. This content is platform-agnostic and survives even if the app were rewritten in a different framework.

| Content                                                                 | Destination                                                    |
| ----------------------------------------------------------------------- | -------------------------------------------------------------- |
| Routes table (URLs the app serves)                                      | `specs/apps/<app-family>/components/web/routes-and-screens.md` |
| Screens table (user-visible pages)                                      | `specs/apps/<app-family>/components/web/routes-and-screens.md` |
| Entry-flow tables                                                       | `specs/apps/<app-family>/components/web/routes-and-screens.md` |
| Bounded-context project layout (full `src/contexts/<bc>/...` recursion) | `specs/apps/<app-family>/components/web/architecture.md`       |
| Layer rules (`domain` ← no imports, etc.)                               | `specs/apps/<app-family>/components/web/architecture.md`       |
| Dormant code listing                                                    | `specs/apps/<app-family>/components/web/architecture.md`       |
| Design system palette / fonts / dark-mode / token import                | `specs/apps/<app-family>/components/web/design-system.md`      |
| Component variant catalog                                               | `specs/apps/<app-family>/components/web/design-system.md`      |
| API endpoints table                                                     | `specs/apps/<app-family>/components/be/api.md`                 |
| Backend architecture diagram (DI, project tree)                         | `specs/apps/<app-family>/components/be/api.md`                 |
| Backend testing strategy                                                | `specs/apps/<app-family>/components/be/api.md`                 |
| E2E architecture (bddgen pipeline, feature → spec → test flow)          | `specs/apps/<app-family>/<owner>/behaviours/README.md`         |

**Applying the rule — three questions in order:**

1. Does this section answer "how do I run THIS checkout?" → Category A, keep.
2. Does this section answer "what does THIS app do (regardless of framework)?" → Category B, move.
3. Both? → Split. The "what" part moves; a one-line "see `specs/`..." stays in the README.

When a paragraph genuinely fits both categories, bias toward moving. The app README must stay thin.
