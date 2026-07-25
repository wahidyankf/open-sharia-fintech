# E2E fixture manifests

Fixture `PathManifest` JSON files for the `ayokoding-www-fe-e2e` course-paths scenarios
(`ayokoding-learning-path-03-navigation-ui` plan, Phase 3). The real
`apps/ayokoding-www/src/features/course-paths/manifests/` directory is still unpopulated (a
downstream content-authoring concern, out of this plan's scope), so every course-paths e2e scenario
that needs a populated hub/category/arc/path landing points its server at this directory instead via
`AYOKODING_WEB_MANIFESTS_DIR`:

- Locally: `playwright.config.ts`'s own `webServer.env`.
- In CI: `infra/dev/ayokoding-www/docker-compose.yml`'s `environment`, backed by the
  `apps/ayokoding-www/Dockerfile`'s `COPY apps/ayokoding-www-fe-e2e/fixtures/manifests ...` step.

## Fixture set

| pathId                                          | arc                       | courseOrder | Purpose                                                                                                                                           |
| ----------------------------------------------- | ------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| `careers/interview-ready/backend-track`         | `interview-ready`         | 2 courses   | Sole role of its arc — arc-landing one-role scenario. Shares `just-enough-python` with `immediately-effective/frontend-track` (multi-badge case). |
| `careers/immediately-effective/frontend-track`  | `immediately-effective`   | 2 courses   | First of two roles — arc-landing two-role scenario.                                                                                               |
| `careers/immediately-effective/backend-track`   | `immediately-effective`   | 3 courses   | Second of two roles, deliberately a different course count than its sibling.                                                                      |
| `careers/fundamentally-strong/generalist-track` | `fundamentally-strong`    | 2 courses   | Third fixture arc — careers category-landing arc-chooser scenario (three arcs, not two).                                                          |
| `skills/e2e-fixture-alpha`                      | `e2e-fixture-alpha-track` | 2 courses   | Paired with `e2e-fixture-beta` for the skills path-landing-body scenario (distinct authored bodies, no cross-leak).                               |
| `skills/e2e-fixture-beta`                       | `e2e-fixture-beta-track`  | 2 courses   | See above.                                                                                                                                        |

The `skills/e2e-fixture-{alpha,beta}` manifests each have a matching real content page under
`apps/ayokoding-www/content/en/learn/paths/skills/e2e-fixture-{alpha,beta}/_index.md` supplying the
authored runway-justification body the skills path-landing-body scenario asserts on. There is no
`AYOKODING_WEB_CONTENT_DIR`-style content-fixture override for e2e (unlike the manifests directory
above): the content repository's directory override is global to the whole site, so redirecting it
to a fixture-only tree would also replace every other real content page other e2e scenarios depend
on (e.g. `just-enough-python`, `sql-essentials`). These two pages are therefore authored `draft:
true` in the real content tree instead, so they never render on prod-ayokoding-www; both
`playwright.config.ts`'s `webServer.env` (local) and `docker-compose.yml`'s `environment` (CI) set
`AYOKODING_WEB_SHOW_DRAFTS=true` so the e2e server still renders them.

The category-landing/arc-landing **empty**-state scenario is deliberately NOT covered by adding a
"zero-manifest" fixture: `resolvePathsRoute`/`manifestsForArc` already render the empty state for
any syntactically valid arc slug this fixture set does not define (e.g.
`/en/learn/paths/careers/no-fixture-arc/`), so no separate empty fixture is needed.
