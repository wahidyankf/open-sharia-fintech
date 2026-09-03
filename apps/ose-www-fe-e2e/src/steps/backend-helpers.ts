/**
 * Shared helpers for the backend BDD step files. Every backend scenario drives the same live
 * server (`webServer` in playwright.config.ts) over HTTP via Playwright's `request` fixture — this
 * builds the tRPC batch-query URL shape the app's `/api/trpc/[trpc]` route expects, and unwraps its
 * response envelope.
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
