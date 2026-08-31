# OSE Family Specs

Platform-agnostic specifications for all OSE-family deployables. Two distinct products share this
tree:

- **OSE Application** (`ose-app-*`) — AI-assisted GRC platform (app.oseplatform.com).
  F#/Giraffe backend + Next.js 16 frontend.
- **OSE Platform Web** (`ose-www`) — Marketing and updates site
  (oseplatform.com). Next.js 16 + tRPC, single container.

## 🧭 Start here

- Exploring the product purpose? Read [product/](./product/README.md) first, then choose the OSE
  Application or OSE Platform Web section below.
- Planning a change? Follow [system-context/](./system-context/README.md),
  [containers/](./containers/README.md), and [components/](./components/README.md) from broad to
  specific.
- Checking an expected outcome? Go to [behavior/](./behavior/README.md) and then its matching
  Gherkin feature.

## Structure

```
specs/apps/ose/
├── README.md                   # This file
├── product/                    # Product framing (above C4) — both products
├── system-context/             # C4 L1 — actors and external systems
├── containers/                 # C4 L2 — deployable units (+ contracts/)
│   └── contracts/              # OpenAPI 3.1 contract spec (ose-app only)
├── components/                 # C4 L3 — per-container internals
│   ├── be/                     # ose-be (F#/Giraffe) component specs
│   ├── platform-be/            # ose-www tRPC HTTP perspective
│   └── platform-web/           # ose-www UI perspective
└── behavior/                   # Gherkin scenarios
    ├── be/gherkin/             # ose-be HTTP-semantic scenarios
    ├── app-web/gherkin/        # ose-app-web UI-semantic scenarios
    ├── platform-be/gherkin/    # ose-www tRPC HTTP-semantic scenarios
    └── platform-web/gherkin/   # ose-www UI-semantic scenarios
```

## OSE Application (`ose-app-*`)

GRC fullstack: AI-assisted gap analysis between regulatory documents and internal policies.

### Behavior Surfaces

| Surface   | Perspective                             | Background                 | Consumers                                   |
| --------- | --------------------------------------- | -------------------------- | ------------------------------------------- |
| `be`      | HTTP-semantic (GET, POST, status codes) | `Given the API is running` | `apps/ose-be` (F#/Giraffe, TickSpec)        |
| `app-web` | UI-semantic (clicks, types, sees)       | `Given the app is running` | `apps/ose-app-web` (Next.js 16, Playwright) |

### Bounded Contexts (ose-app)

| Bounded Context     | `be` features | Description                                                             |
| ------------------- | :-----------: | ----------------------------------------------------------------------- |
| `health`            |       1       | Liveness endpoint — service health to orchestrators                     |
| `regulatory-source` |       —       | Ingests regulator-published rule documents with provenance metadata     |
| `internal-policy`   |       —       | Ingests company-internal documents (SOPs, manuals, procedures)          |
| `gap-analysis`      |       —       | Compares regulatory corpus against policy corpus; emits GapItem records |
| `ai-orchestration`  |       —       | Wraps LLM calls (OpenRouter), prompt management, retry/backoff          |

## OSE Platform Web (`ose-www`)

Content and marketing site for the OSE Platform.

### Behavior Surfaces

| Surface        | Perspective                             | Background                 | Consumers             |
| -------------- | --------------------------------------- | -------------------------- | --------------------- |
| `platform-be`  | tRPC HTTP-semantic (procedures, routes) | `Given the API is running` | `apps/ose-www-be-e2e` |
| `platform-web` | UI-semantic (clicks, types, sees)       | `Given the app is running` | `apps/ose-www-fe-e2e` |

### Bounded Contexts (ose-www)

| Bounded Context | `platform-web` features | `platform-be` features | Description                                                           |
| --------------- | :---------------------: | :--------------------: | --------------------------------------------------------------------- |
| `app-shell`     |            4            |           —            | Header, footer, theme toggle, navigation, responsive, accessibility   |
| `landing`       |            1            |           —            | Marketing landing page at `/`                                         |
| `content`       |            —            |           1            | Content retrieval (tRPC procedures + filesystem adapters + rendering) |
| `search`        |            —            |           1            | Search backend (tRPC + index) + UI                                    |
| `rss-feed`      |            —            |           1            | RSS 2.0 feed generation route handler                                 |
| `seo`           |            —            |           1            | Sitemap, robots, per-route metadata                                   |
| `health`        |            —            |           1            | Health probe (tRPC) + system-status diagnostic page                   |

## Spec Artifacts

- **[containers/](./containers/README.md)** — C4 architecture diagrams (L2)
- **[containers/contracts/](./containers/contracts/README.md)** — OpenAPI 3.1 contract spec
  (ose-app only); generates types for ose-be and ose-app-web via `codegen` Nx target
- **[components/](./components/README.md)** — C4 component diagrams (L3) per surface
- **[behavior/](./behavior/README.md)** — Gherkin acceptance criteria

## Related

- [Three-Level Testing Standard](../../../repo-governance/development/quality/three-level-testing-standard.md)
- [BDD Spec-Test Mapping](../../../repo-governance/development/infra/bdd-spec-test-mapping.md)
- [apps/ose-be/](../../../apps/ose-be/README.md)
- [apps/ose-app-web/](../../../apps/ose-app-web/README.md)
- [apps/ose-www/](../../../apps/ose-www/README.md)
