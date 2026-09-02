/**
 * Placeholder step definitions for the organiclever-www BE E2E slot.
 *
 * organiclever-www is a pure marketing site with no backend API (no tRPC
 * route handlers). This project exists to satisfy the standardized
 * {app}-be-e2e + {app}-fe-e2e reusable workflow pair. The be-e2e slot is
 * tolerated-absent in CI (called with `|| true`) and holds no real scenarios.
 *
 * Covers: specs/apps/organiclever/www/behaviors/backend/placeholder/placeholder.feature
 */
import { createBdd } from "playwright-bdd";

const { Given } = createBdd();

// Background step used by the placeholder scenario.
Given("no backend API exists for organiclever-www", async () => {
  // No-op: organiclever-www is a static marketing site with no backend API.
});
