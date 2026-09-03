/**
 * Shared helpers for the backend BDD step files. Every backend scenario drives the same live
 * server (`webServer` in playwright.config.ts) over HTTP via Playwright's `request` fixture — this
 * builds the tRPC batch-query URL shape the app's `/api/trpc/[trpc]` route expects, and unwraps its
 * response envelope. Identical shape to ayokoding-www-be-e2e's own
 * `tests/integration/steps/helpers.ts` (this project's integration-level sibling covering the same
 * corpus), kept as an independent copy per project rather than a shared import since the two
 * projects have no shared TypeScript package boundary between their `tests/` trees.
 */
export function buildTrpcUrl(procedure: string, input: unknown): string {
  const encoded = encodeURIComponent(JSON.stringify({ "0": { json: input } }));
  return `/api/trpc/${procedure}?batch=1&input=${encoded}`;
}

export function extractTrpcData(body: unknown): unknown {
  const arr = body as { result: { data: { json: unknown } } }[];
  return arr[0]?.result?.data?.json;
}

// Shared mutable state for cross-step communication within one backend scenario.
export const backendState: Record<string, unknown> = {};
