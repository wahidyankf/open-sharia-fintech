Feature: organiclever-www has no backend API

  organiclever-www is a pure Next.js static marketing site.
  It has no tRPC route handlers or dedicated backend.
  This slot exists to satisfy the standardized www reusable workflow pair
  (be-e2e + fe-e2e), where be-e2e is tolerated-absent in CI.

  Scenario: no backend API scenarios exist for organiclever-www
    Given no backend API exists for organiclever-www
