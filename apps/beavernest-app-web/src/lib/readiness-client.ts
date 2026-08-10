import type { ReadinessReady, ReadinessUnavailable } from "../generated-contracts";

export type ReadinessResponse = ReadinessReady | ReadinessUnavailable;

/**
 * Narrows an unknown network body to the closed `ReadinessResponse` union by
 * checking the discriminant the backend contract fixes both members to.
 * `response.json()` is typed `Promise<any>` — this is the one place that
 * shape is actually verified before the rest of the app trusts it.
 */
function isReadinessResponse(body: unknown): body is ReadinessResponse {
  return (
    typeof body === "object" &&
    body !== null &&
    "status" in body &&
    (body.status === "ready" || body.status === "not-ready")
  );
}

export async function fetchReadiness(signal?: AbortSignal): Promise<ReadinessResponse> {
  const response = await fetch("/api/v1/readiness", { signal });
  const body: unknown = await response.json();

  if ((!response.ok && response.status !== 503) || !isReadinessResponse(body)) {
    throw new Error("The foundation status could not be loaded.");
  }

  return body;
}
