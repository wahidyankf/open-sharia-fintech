# OrganicLever Frontend Gherkin Specs

Gherkin feature files for the OrganicLever frontend application, organized by feature
context. Each folder groups a related product capability.

## Structure

```
specs/apps/organiclever/app-web/behaviours/
├── app-shell/             # Navigation, cross-cutting loggers
│   ├── entry-loggers.feature
│   └── navigation.feature
├── health/                # Backend health diagnostic page
│   └── system-status-be.feature
├── journal/               # Journal events — today's entries, filtering
│   └── home-screen.feature
├── routine/               # Workout routine management
│   └── routine-management.feature
├── routing/               # App routing and 404 guards
│   ├── app-routes.feature
│   └── disabled-routes.feature
├── settings/              # User preferences (dark mode, language)
│   ├── dark-mode.feature
│   ├── language.feature
│   └── settings-screen.feature
├── stats/                 # History and progress projections over journal events
│   ├── history-screen.feature
│   └── progress-screen.feature
└── workout-session/       # Active workout session FSM
    └── workout-session.feature
```

## Conventions

- **File naming**: `[domain-capability].feature` (kebab-case)
- **Step language**: UI-semantic only — clicks, types, sees, navigates (no HTTP verbs or
  status codes)
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`
- **Term discipline**: Step text uses product language, not implementation identifiers or route
  segments

## Relationship to organiclever-be

These specs are the **frontend counterpart** to
[be/gherkin/](../../be/behaviours/README.md). The two trees cover different domains:

- **be**: HTTP-semantic (GET, POST, status codes, response bodies)
- **fe**: UI-semantic (clicks, types, sees, navigates, form submissions)

`apps/organiclever-app-web` consumes these specs via `@amiceli/vitest-cucumber` step
definitions in `apps/organiclever-app-web/tests/unit/steps/`.

## Related

- **Backend counterpart**: [be gherkin specs](../../be/behaviours/README.md)
- **Parent**: [web component specs](../architecture.md)

- [app-shell](./app-shell/README.md) — organiclever-app-web Gherkin Domain
- [health](./health/README.md) — organiclever-app-web Gherkin Domain
- [journal](./journal/README.md) — organiclever-app-web Gherkin Domain
- [routine](./routine/README.md) — organiclever-app-web Gherkin Domain
- [routing](./routing/README.md) — organiclever-app-web Gherkin Domain
- [settings](./settings/README.md) — organiclever-app-web Gherkin Domain
- [stats](./stats/README.md) — organiclever-app-web Gherkin Domain
- [workout-session](./workout-session/README.md) — organiclever-app-web Gherkin Domain
