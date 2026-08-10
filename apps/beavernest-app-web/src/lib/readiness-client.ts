import type { ReadinessReady, ReadinessUnavailable } from "../generated-contracts";

export type ReadinessResponse = ReadinessReady | ReadinessUnavailable;

export async function fetchReadiness(signal?: AbortSignal): Promise<ReadinessResponse> {
  const response = await fetch("/api/v1/readiness", { signal });
  const body = (await response.json()) as ReadinessResponse;

  if (!response.ok && response.status !== 503) {
    throw new Error("The foundation status could not be loaded.");
  }

  return body;
}
