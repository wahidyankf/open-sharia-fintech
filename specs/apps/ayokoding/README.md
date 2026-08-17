# AyoKoding Application Specs

Platform-agnostic specifications for the AyoKoding educational website. AyoKoding ships
multilingual programming, AI, and security tutorials in English (primary) and Indonesian.
The application is rolling-release on `main` (Trunk Based Development).

The system is implemented as a single Next.js 16 application that serves both server-rendered
HTML pages (App Router) and a tRPC HTTP API at `/api/trpc/*`. There is no separate backend
container.

## 🧭 Start here

- Want to understand the learning product and its audience? Start with
  [product/](./product/README.md).
- Need to see a user journey or API promise? Browse [behavior/](./behavior/README.md), then the
  relevant Gherkin feature.
- Mapping an implementation change? Use [system-context/](./system-context/README.md),
  [containers/](./containers/README.md), and [components/](./components/README.md) in that order.

## Structure

```
specs/apps/ayokoding/
├── README.md              # This file
├── product/               # Product framing (above C4)
│   └── README.md
├── system-context/        # C4 L1 — actors and external systems
│   ├── README.md
│   └── context.md
├── containers/            # C4 L2 — deployable units (one: `web`)
│   ├── README.md
│   └── container.md
├── components/            # C4 L3 — per-perspective internals
│   ├── README.md
│   ├── api/               # tRPC API perspective (HTTP-semantic)
│   │   ├── README.md
│   │   └── component-api.md
│   └── web/               # UI perspective (browser interaction)
│       ├── README.md
│       └── component-web.md
├── ddd/                   # DDD artifacts (platform-agnostic; shared by all surfaces)
│   ├── README.md
│   ├── bounded-contexts.yaml
│   ├── bounded-context-map.md
│   └── ubiquitous-language/
│       ├── README.md
│       └── *.md           # One glossary file per bounded context
└── behavior/              # Gherkin scenarios (all surfaces)
    ├── README.md
    ├── ayokoding-be/gherkin/          # tRPC API scenarios (per bounded context)
    ├── ayokoding-build-tools/gherkin/ # Build-time index-generation scripts
    │   └── index-generation/
    ├── ayokoding-cli/gherkin/         # Link-validation CLI scenarios
    └── ayokoding-www/gherkin/         # Browser UI scenarios (per bounded context)
```

## Containers and perspectives

AyoKoding ships **one deployable container**: `web` (Next.js 16). The Gherkin behavior tree
splits along **API perspective** — `web` (UI-semantic) vs `api` (tRPC HTTP-semantic) — not
along container boundaries. Both perspectives execute inside the same `web` container.

| Perspective | Background                 | Scenarios                                                                     | Domains covered                                                          | Consumed by                              |
| ----------- | -------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------- |
| `web`       | `Given the app is running` | [behavior/ayokoding-www/gherkin/](./behavior/ayokoding-www/gherkin/README.md) | app-shell (responsive, accessibility), content, search, i18n, navigation | `apps/ayokoding-www` (Playwright FE E2E) |
| `api`       | `Given the API is running` | [behavior/ayokoding-be/gherkin/](./behavior/ayokoding-be/gherkin/README.md)   | content, search, navigation, i18n, health                                | `apps/ayokoding-www` (Playwright BE E2E) |

The slug `api` is a **perspective slug**, not a container. There is no separate API
container — tRPC procedures execute inside the same `web` container's Next.js server. The
`organiclever` peer keeps the legacy slug `be` because `organiclever-be` is a real
F#/Giraffe container; ayokoding does not have one and never will under the current
architecture.

## Bounded Contexts

Counts are Gherkin features per perspective. `--` means no features in that perspective.

| Bounded Context | `web` features | `api` features | Description                                             |
| --------------- | -------------- | -------------- | ------------------------------------------------------- |
| app-shell       | 2              | --             | Responsive layout + accessibility chrome                |
| content         | 1              | 1              | Content rendering + tRPC content procedures             |
| search          | 1              | 1              | Search dialog + tRPC search procedures                  |
| i18n            | 1              | 1              | Locale switcher + tRPC locale data + Next.js middleware |
| navigation      | 3              | 1              | Top-level navigation + tRPC navigation tree             |
| health          | --             | 1              | Service liveness probe                                  |

## Spec Artifacts

- **[system-context/](./system-context/README.md)**, **[containers/](./containers/README.md)**,
  **[components/](./components/README.md)** — C4 architecture diagrams (L1/L2/L3)
- **[components/api/](./components/api/README.md)** — API (tRPC HTTP-semantic) component specs
  ([Gherkin features](./behavior/ayokoding-be/gherkin/README.md))
- **[components/web/](./components/web/README.md)** — Web (UI-semantic) component specs
  ([Gherkin features](./behavior/ayokoding-www/gherkin/README.md))

## DDD Registry (`bounded-contexts.yaml`)

`bounded-contexts.yaml` is the machine-readable declaration of every bounded context in
`ayokoding-www`. `specs structure validate` reads it in two rule layers (`bc:` and `ul:`) to enforce structural and
vocabulary invariants automatically in `npm exec nx -- run ayokoding-www:test:quick`.

### Schema

Each entry under `contexts:` declares:

| Field           | What it means                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `name`          | Identifier — must match the folder name under `src/contexts/`                                                 |
| `summary`       | One-paragraph human description                                                                               |
| `layers`        | Ordered list of DDD layers that must exist as subfolders (e.g. `[application, infrastructure, presentation]`) |
| `code`          | Filesystem path to the context's implementation root                                                          |
| `glossary`      | Path to the context's ubiquitous-language Markdown file                                                       |
| `gherkin`       | Path to the context's Gherkin scenario directory                                                              |
| `relationships` | List of inter-context relationships with `to`, `kind`, and `role`                                             |

Relationship `kind` values: `customer-supplier`, `conformist`, `shared-kernel`.
For `customer-supplier` and `conformist`, both sides must declare the relationship
(symmetry enforced by the `bc:` layer).

### Multi-perspective `gherkin:` workaround

Today's `bcregistry/Context.Gherkin` is a single string. Four ayokoding BCs span both
perspectives (`content`, `search`, `i18n`, `navigation`). The registry can only point at
one path per BC, so each multi-perspective BC registers its **web-side** path. The api-side
features (`content-api.feature`, `search-api.feature`, `i18n-api.feature`,
`navigation-api.feature`) are still validated by the `specs:coverage` target (which runs
against both perspectives independently), but are not walked by the `bc:` layer for that BC's
`gherkin:` field. This limitation is tracked in the `bdd-ddd-tooling-gap-fill` plan
(fix #11: `gherkin: []string` schema extension).

### The `bc:` layer — structural parity

Reads the registry and verifies the **filesystem** matches exactly:

- Every declared `code:` path exists with **exactly** the declared `layers:` subfolders
  (extra or missing layer = error)
- Every declared `glossary:` file exists on disk
- Every declared `gherkin:` directory exists and contains ≥1 `.feature` file
- No **orphan** directories exist under `src/contexts/` that aren't in the registry
- Relationship declarations are symmetric across both context entries

### The `ul:` layer — glossary parity

Reads the registry to locate every `glossary:` file, then validates each:

- Required frontmatter keys present (`Bounded context`, `Maintainer`, `Last reviewed`)
- Terms table header matches canonical columns
- Code identifiers (backtick-wrapped in the table) exist somewhere in the declared
  `code:` path — stale identifiers from renamed types or deleted functions are caught here
- Feature file references in the table resolve to real `.feature` files under the
  declared `gherkin:` path
- Same term in two glossaries → both must carry mutual `Forbidden-synonyms` cross-links

### Adding a new bounded context

1. Add an entry to `bounded-contexts.yaml` with all six fields.
2. Create the code directory with the declared layer subfolders under
   `apps/ayokoding-www/src/contexts/<bc>/`.
3. Create the glossary file at `ddd/ubiquitous-language/<bc>.md`.
4. Create the gherkin directory and add at least one `.feature` file under
   `behavior/ayokoding-www/gherkin/<bc>/` (and optionally `behavior/ayokoding-be/gherkin/<bc>/`).
5. Run `npm exec nx -- run ayokoding-www:test:quick` — the `bc:` and `ul:` layers confirm
   the registry matches the filesystem before any unit tests run.

## tRPC Procedures

The `web` container exposes these tRPC procedures (all under one Next.js process):

| Procedure              | BC         | Description                           |
| ---------------------- | ---------- | ------------------------------------- |
| `content.getBySlug`    | content    | Fetch a single page by its slug       |
| `content.listChildren` | content    | List direct children of a section     |
| `content.getTree`      | navigation | Fetch full navigation tree for locale |
| `search.query`         | search     | Full-text search within a locale      |
| `meta.health`          | health     | Service liveness status               |
| `meta.languages`       | i18n       | Available locales                     |

## Spec Consumption

The `web` container consumes specs at two test levels:

- **`test:quick`** — Vitest unit tests + coverage check; Gherkin spec paths are
  included in Nx cache inputs so cache invalidates when specs change
- **`test:e2e`** (BE + FE) — Playwright drives the running Next.js app

## Related

- [Three-Level Testing Standard](../../../repo-governance/development/quality/three-level-testing-standard.md)
- [BDD Spec-Test Mapping](../../../repo-governance/development/infra/bdd-spec-test-mapping.md)
- [BDD Standards](../../../docs/explanation/software-engineering/development/behavior-driven-development-bdd/README.md)
- [apps/ayokoding-www/](../../../apps/ayokoding-www/README.md) — Next.js implementation
- [apps/ayokoding-cli/](../../../apps/ayokoding-cli/README.md) — CLI tool (content link validation)
