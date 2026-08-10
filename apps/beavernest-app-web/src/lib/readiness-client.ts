import type { ReadinessReady, ReadinessUnavailable } from "../generated-contracts";

export type ReadinessResponse = ReadinessReady | ReadinessUnavailable;

/**
 * Both `ReadinessResponse` union members fix `components` to a `{ database,
 * schema }` pair whose values are `const`-pinned per `status`
 * (`specs/apps/beavernest/containers/contracts/openapi.yaml`,
 * `additionalProperties: false`, `required: [status, components]`).
 */
function hasValidComponents(status: "ready" | "not-ready", body: Record<string, unknown>): boolean {
  if (!("components" in body) || typeof body.components !== "object" || body.components === null) {
    return false;
  }

  const components = body.components as Record<string, unknown>;

  return status === "ready"
    ? components.database === "ready" && components.schema === "current"
    : components.database === "unavailable" && components.schema === "unknown";
}

/**
 * Narrows an unknown network body to the closed `ReadinessResponse` union by
 * checking both fields the backend contract requires: the `status`
 * discriminant and the `components` shape each `status` value fixes.
 * `response.json()` is typed `Promise<any>` — this is the one place that
 * shape is actually verified before the rest of the app trusts it.
 */
function isReadinessResponse(body: unknown): body is ReadinessResponse {
  if (typeof body !== "object" || body === null || !("status" in body)) {
    return false;
  }

  const status = (body as Record<string, unknown>).status;

  if (status !== "ready" && status !== "not-ready") {
    return false;
  }

  return hasValidComponents(status, body as Record<string, unknown>);
}

export async function fetchReadiness(signal?: AbortSignal): Promise<ReadinessResponse> {
  const response = await fetch("/api/v1/readiness", { signal });
  const body: unknown = await response.json();

  if ((!response.ok && response.status !== 503) || !isReadinessResponse(body)) {
    throw new Error("The foundation status could not be loaded.");
  }

  return body;
}
