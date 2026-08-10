import { http, HttpResponse } from "msw";
import type { ReadinessReady, ReadinessUnavailable } from "../../generated-contracts";

export const readinessReady: ReadinessReady = {
  status: "ready",
  components: { database: "ready", schema: "current" },
};

export const readinessUnavailable: ReadinessUnavailable = {
  status: "not-ready",
  components: { database: "unavailable", schema: "unknown" },
};

export const readinessHandler = http.get("*/api/v1/readiness", () => HttpResponse.json(readinessReady));
