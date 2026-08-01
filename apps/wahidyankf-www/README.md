# wahidyankf-www

Personal portfolio / CV / projects site for Wahidyan Kresna Fridayoka.
Adopted from [`wahidyankf/oss / apps-standalone/wahidyankf-web`](https://github.com/wahidyankf/oss/tree/main/apps-standalone/wahidyankf-web)
in 2026-04 and retrofitted to the `ose-public` Nx monorepo conventions.

**Framework**: Next.js 16 (App Router) · React 19 · Tailwind CSS 4
**Language**: TypeScript
**Deployment**: Vercel via `prod-wahidyankf-www` branch
**Production domain**: <https://www.wahidyankf.com/>
**Dev port**: 3201

## Development

```bash
# Start the dev server (localhost:3201)
nx dev wahidyankf-www

# Production build
nx build wahidyankf-www

# Local production preview
nx start wahidyankf-www
```

## Quality gates

```bash
# Type check only
nx run wahidyankf-www:typecheck

# oxlint + jsx-a11y
nx run wahidyankf-www:lint

# Unit tests (Vitest 4, jsdom)
nx run wahidyankf-www:test:unit

# Fast pre-push gate: unit tests + coverage ≥80%
nx run wahidyankf-www:test:quick

# Integration tests (node environment; empty at adoption time)
nx run wahidyankf-www:test:integration

# Gherkin spec coverage check
nx run wahidyankf-www:specs:coverage
```

## Testing stack

- **Vitest 4** + `@vitejs/plugin-react` + `jsdom` for unit tests
- **`@amiceli/vitest-cucumber`** for Gherkin acceptance specs at the unit
  level (feature files under `specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/`)
- **`@testing-library/react`** + **`@testing-library/jest-dom`** for
  component interaction
- Coverage enforced at ≥80% via `vitest --coverage.thresholds.lines=80` —
  aligned to `apps/ayokoding-www` and `apps/ose-www`

End-to-end tests live in the sibling project `apps/wahidyankf-www-fe-e2e/`
using Playwright-BDD and `@axe-core/playwright` for WCAG 2.1 AA smoke.

## Specs

Platform-agnostic specifications for this app live at
[`specs/apps/wahidyankf/`](../../specs/apps/wahidyankf/README.md):

- **Five-folder C4 tree**: `product/`, `system-context/`, `containers/`,
  `components/`, `behavior/`
- **Gherkin features**:
  [`specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/`](../../specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/README.md) —
  feature files organized per feature module

## Architecture

This app uses the repo-standard functional-core / imperative-shell feature-module layout
(`src/features/<name>/{core,shell}/`) shared by all Next.js web apps — defined in
[`repo-governance/development/pattern/functional-core-imperative-shell-web.md`](../../repo-governance/development/pattern/functional-core-imperative-shell-web.md).
Because this is a static portfolio, most features are shell-only, with pure CV/project/search data and helpers in
`core/`.

Each feature splits into two layers:

- **`core/`** — functional core: pure functions, immutable data, plain types, and constant
  data tables. Never imports `react`, `next`, or node builtins, and never imports `shell/`.
- **`shell/`** — imperative shell: React components, DOM-touching hooks, and anything
  effectful. May import its own and sibling `core/`.

Each feature directory is self-contained and imports only from sibling features or shared
libraries.

## Deployment

`prod-wahidyankf-www` branch receives force-pushes from `main` via the
`apps-wahidyankf-www-deployer` agent. Vercel watches the branch and
rebuilds on every push.

## Structure

```
apps/wahidyankf-www/
├── public/                   # Static assets (favicon, fonts)
├── src/
│   ├── app/                  # Next.js App Router routing shell (thin wrappers)
│   │   ├── cv/page.tsx       # Routes to CvContent from cv feature
│   │   ├── personal-projects/page.tsx
│   │   ├── fonts/            # GeistVF, GeistMonoVF woff
│   │   ├── layout.tsx
│   │   ├── head.tsx
│   │   ├── page.tsx          # Routes to HomeContent from home feature
│   │   └── globals.css       # Tailwind 4 entry
│   ├── features/             # Feature modules (core = pure, shell = UI/IO)
│   │   ├── app-shell/
│   │   │   ├── core/         # style.ts (cn class-name utility)
│   │   │   └── shell/        # Navigation.tsx
│   │   ├── cv/
│   │   │   ├── core/         # data.ts (CVEntry, cvData, helpers)
│   │   │   └── shell/        # markdown.tsx, CvContent.tsx
│   │   ├── home/
│   │   │   └── shell/        # HomeContent.tsx
│   │   ├── personal-projects/
│   │   │   ├── core/         # projects.ts (Project, filterProjects)
│   │   │   └── shell/        # PersonalProjectsContent.tsx
│   │   └── search/
│   │       ├── core/         # search.ts (filterItems, SearchTerm, SearchResult)
│   │       └── shell/        # SearchSection.tsx
│   └── test/setup.ts         # Vitest + Testing Library setup
└── test/unit/steps/          # Gherkin step implementations
```
