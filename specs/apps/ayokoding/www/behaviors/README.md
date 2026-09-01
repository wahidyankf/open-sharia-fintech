# AyoKoding Web — Behaviors

The recursive Gherkin corpus for `ayokoding-www`. A scenario here is the contract; the step
definitions in `apps/ayokoding-www/test/` and the two E2E projects implement it.

## Contents

- [Frontend](./frontend/README.md) — what a learner sees: content rendering, navigation, search,
  locale switching, accessibility, and responsive layout.
- [Backend](./backend/README.md) — what a tRPC procedure returns: content, navigation, search,
  i18n, and health, including error codes and locale scoping.
- [Build tools](./build-tools/README.md) — what the build-time index generators must produce
  before the site is built.

## Related

- [Architecture](../architecture.md) — the system these scenarios describe.
- [`apps/ayokoding-www/README.md`](../../../../../apps/ayokoding-www/README.md) — the implementing project.
