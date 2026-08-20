# OSE Platform website

`ose-www` is the public website for Open Sharia Enterprise (OSE), available at
[oseplatform.com](https://oseplatform.com). It gives product people and early engineers a clear
starting point for understanding OSE: why trustworthy, Sharia-compliant enterprise products need
to be designed as inspectable systems, what the platform is exploring, and how that work is
developing.

OSE is pre-alpha. The product direction, technical architecture, and public APIs can change as the
team learns. For the wider product context, see the repository
[roadmap](../../roadmap.md) and [application map](../../docs/reference/system-architecture/applications.md).

## What the site provides

- A public introduction to the OSE Platform and its product intent.
- An About page that explains the problem space and current approach.
- A chronological updates section, plus an RSS feed, for published progress and decisions.
- Search across the site's Markdown content.

The site is a Next.js 16 application using the App Router, TypeScript, Tailwind CSS, tRPC, and
Markdown content stored in this app. Its feature modules keep decision-making code in `core/` and
framework or IO work in `shell/`.

## Run locally

From the repository root, install the workspace dependencies and start the site:

```bash
npm install
npm exec nx -- run ose-www:dev
```

Open <http://localhost:3100>. The development server uses port 3100 unless `OSE_WWW_PORT` names
another one. No local configuration is required for the standard site; that variable and the other
optional content and development-server settings are documented in
[.env.example](./.env.example).

For supported platforms, prerequisites, and recovery steps, follow
[Getting started with OSE Public](../../docs/tutorials/getting-started-with-ose-public.md).

## Publish or revise site content

The public pages and updates live in [`content/`](./content/). Update Markdown there to change
what the website publishes:

- `about.md` supplies the About page.
- `updates/_index.md` supplies the updates landing page.
- `updates/<date>-<slug>.md` supplies an individual update.

Each content file uses YAML frontmatter. `title` is required; `description`, `summary`, `date`,
`tags`, `categories`, `draft`, `weight`, `showtoc`, and `url` are supported when applicable. Build
the site after a content change to regenerate its search data and check the rendered result.

## Develop and verify

Run these commands from the repository root:

```bash
# Create the production build (also regenerates search data)
npm exec nx -- run ose-www:build

# Run the focused quality gate: typecheck, lint, unit tests, coverage, and spec checks
npm exec nx -- run ose-www:test:quick

# Run the unit suite only
npm exec nx -- run ose-www:test:unit

# Run the website's companion frontend E2E suite
npm exec nx -- run ose-www-fe-e2e:test:e2e
```

The focused quality gate enforces 86% line coverage. `ose-www:test:integration` currently reports
that integration testing is not applicable; it is not a substitute for the companion E2E suite.

## Project layout

```text
apps/ose-www/
├── content/       # Public Markdown pages and updates
├── public/        # Static site assets
├── src/app/       # Thin Next.js routes
├── src/features/  # Product features, organized into core/ and shell/
├── test/          # Unit and integration test definitions
└── project.json   # Nx targets for development, build, and verification
```

The behavior specifications that describe the web and tRPC perspectives are in
[specs/apps/ose](../../specs/apps/ose/).

## Production delivery

The production site runs on Vercel at <https://oseplatform.com>. A GitHub Actions workflow runs the
website quality gates and E2E checks; when `apps/ose-www/` has changed and the gates pass, it
updates the `prod-ose-www` deployment branch. Vercel builds only from that branch.

Deployment is automated. Do not manually push to `prod-ose-www`; see the
[production workflow](../../.github/workflows/ose-www-test-local-deploy-prod.yml) and
[deployment reference](../../docs/reference/system-architecture/deployment.md) for the current
delivery path.

## Related references

- [Repository onboarding tutorial](../../docs/tutorials/getting-started-with-ose-public.md)
- [OSE specifications](../../specs/apps/ose/README.md)
- [Application architecture](../../docs/reference/system-architecture/applications.md)
