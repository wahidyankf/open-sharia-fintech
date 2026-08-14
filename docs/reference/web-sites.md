---
title: "Web Sites"
description: Every deployable app in this repo — domain, dev port, and production deploy branch.
category: reference
tags:
  - reference
  - apps
  - deployment
created: 2026-08-14
---

# Web Sites

| App                  | Domain                                                   | Port  | Prod Branch                 |
| -------------------- | -------------------------------------------------------- | ----- | --------------------------- |
| ose-www              | [oseplatform.com](https://oseplatform.com)               | 3100  | `prod-ose-www`              |
| ayokoding-www        | [ayokoding.com](https://ayokoding.com)                   | 3101  | `prod-ayokoding-www`        |
| organiclever-www     | [www.organiclever.com](https://www.organiclever.com/)    | 3200  | `prod-organiclever-www`     |
| organiclever-app-web | TBD                                                      | 3202  | `prod-organiclever-app-web` |
| wahidyankf-www       | [www.wahidyankf.com](https://www.wahidyankf.com/)        | 3201  | `prod-wahidyankf-www`       |
| ose-app-web          | [app.oseplatform.com](https://app.oseplatform.com) (TBD) | 3300  | `prod-ose-app-web` (TBD)    |
| ose-be               | api.oseplatform.com (F# / Giraffe / ASP.NET 10)          | 8302  | —                           |
| organiclever-be      | (F# / Giraffe / ASP.NET 10, Kubernetes)                  | 8202  | —                           |
| beavernest-app       | TBD (Flutter Web, same-origin combined runtime)          | 19300 | —                           |
| beavernest-be        | TBD (F# / Giraffe / ASP.NET 10, combined runtime 19300)  | 19320 | —                           |

Each app README at `apps/[app-name]/README.md` covers framework, deployment, E2E tests, and content
details. Staging branches: `stag-organiclever-app-web`, `stag-ose-app-web`.

**See**: [AGENTS.md](../../AGENTS.md), [monorepo-structure.md](./monorepo-structure.md)
