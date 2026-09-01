# OrganicLever Marketing Web — Component Specs

Audience: Engineers, Technical Product/Project Managers

Component-level specifications for the OrganicLever public marketing site
(`apps/organiclever-www`), served at the domain root.

## Surface

`organiclever-www` is a greenfield-simple Next.js 16 marketing site built on the
`features/` module-root shape its sibling www apps share. It carries the landing content
and assets extracted from the former `organiclever-app-web` `landing` context.

- **Framework**: Next.js 16 (App Router, React 19, Tailwind CSS 4)
- **Shape**: `src/app` + `src/features/{home, app-shell}` (flat feature folders)
- **Design system**: `@open-sharia-enterprise/web-ui` + `@open-sharia-enterprise/web-ui-token`
- **No** local-first database, functional-effects runtime, or state-machine library
- **Dev port**: 3200

## Features

- `home` — the marketing landing experience (hero, event-type features, weekly
  rhythm demo, principles, footer).
- `app-shell` — shared layout primitives for the marketing surface.

## Behavior specs

Behavior scenarios for this surface live at
[behavior/organiclever-www/gherkin/](../../behavior/organiclever-www/gherkin/README.md).

## Related

- **Behavior specs**: [organiclever-www gherkin](../../behavior/organiclever-www/gherkin/README.md)
- **App-client component specs**: [app-web component specs](../app-web/README.md)
