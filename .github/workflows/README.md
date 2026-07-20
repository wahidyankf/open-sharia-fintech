# GitHub Actions Workflows

CI/CD workflows for the monorepo. Filenames follow the
[GitHub Actions Workflow Naming Convention](../../repo-governance/development/infra/github-actions-workflow-naming.md);
the [CI Conventions](../../repo-governance/development/infra/ci-conventions.md) define the
reusable-workflow pattern and the twice-daily WIB CRON schedule (with a 2.5-hour staging→prod gap).

## Reusable

| Workflow                                   | Role                                                                                                     |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `_reusable-www-test-local-deploy.yml`      | Full local-stack test pipeline (lint, unit, integration, E2E) then force-push to a `prod-*-www` branch.  |
| `_reusable-app-test-local-deploy-stag.yml` | App-group local-stack pipeline; on pass force-pushes BOTH the `stag-*-app-web` and `stag-*-be` branches. |
| `_reusable-app-test-stag.yml`              | FE E2E gate against the deployed staging URL (Vercel bypass secret). Stops on pass — no promote.         |
| `_reusable-be-build-deploy.yml`            | Build a backend image and push it to GHCR (rolled out by ose-infra `coralpolyp`).                        |

## PR and repo-wide gates

| Workflow              | Trigger                | Role                                                                                                                              |
| --------------------- | ---------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| `pr-quality-gate.yml` | PR + push              | Typecheck, lint, `test:quick`, `compat:min-version`, naming, md-links, harness-duplication, governance validation (all languages) |
| `validate-env.yml`    | PR + push              | Environment-variable contract validation                                                                                          |
| `main-ci.yml`         | 4x/day CRON + dispatch | Same as PR gate but runs across all projects (`nx run-many --all`) — no push trigger                                              |
| `deps-audit.yml`      | Nightly CRON           | Language-native dependency audit (npm audit, cargo deny, dotnet vulnerable) — CRON-only                                           |

## www tier — direct deploy (scheduled callers of `_reusable-www-test-local-deploy.yml`)

| Workflow                                      | Site                                |
| --------------------------------------------- | ----------------------------------- |
| `ayokoding-www-test-local-deploy-prod.yml`    | ayokoding-www → ayokoding.com       |
| `ose-www-test-local-deploy-prod.yml`          | ose-www → oseplatform.com           |
| `organiclever-www-test-local-deploy-prod.yml` | organiclever-www → organiclever.com |
| `wahidyankf-www-test-local-deploy-prod.yml`   | wahidyankf-www → www.wahidyankf.com |

## app tier — gated promotion (local-deploy-stag → test-stag; prod CD deferred)

| Workflow                                      | Stage                                                            |
| --------------------------------------------- | ---------------------------------------------------------------- |
| `organiclever-app-test-local-deploy-stag.yml` | Test the organiclever app group, force-push web + be stag branch |
| `organiclever-app-test-stag.yml`              | FE E2E gate vs staging (+2.5h); stops on pass                    |
| `ose-app-test-local-deploy-stag.yml`          | Test the ose-app group, force-push web + be stag branch          |
| `ose-app-test-stag.yml`                       | FE E2E gate vs staging (+2.5h); stops on pass                    |

## Backend images and CLIs

| Workflow                                | Role                                                                                                                        |
| --------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `publish-images.yml`                    | Build and push `organiclever-be` / `ose-be` images to GHCR (deployed by the ose-infra k3s plans, not Vercel) — transitional |
| `organiclever-be-build-deploy-stag.yml` | Build the `organiclever-be` image and push it to GHCR; triggered on `stag-organiclever-be` push                             |
| `ose-be-build-deploy-stag.yml`          | Build the `ose-be` image and push it to GHCR; triggered on `stag-ose-be` push                                               |

## web-ui — Storybook (scheduled deploy)

| Workflow                       | Trigger                           | Role                                                                          |
| ------------------------------ | --------------------------------- | ----------------------------------------------------------------------------- |
| `web-ui-build-deploy-prod.yml` | Daily CRON (00:00 UTC) + dispatch | Build the `web-ui` lib's Storybook and force-push the output to `prod-web-ui` |
