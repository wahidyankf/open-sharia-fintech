import type { APIResponse, Page } from "@playwright/test";

/**
 * `page.request.get()` wrapped with a single retry.
 *
 * Full-suite parallel runs (`fullyParallel: true`, `workers: undefined` locally) open hundreds
 * of concurrent connections against one local production server instance (`webServer` in
 * `playwright.config.ts` boots a single `node server.js`). Under that contention the server
 * occasionally drops a connection mid-handshake (`ECONNRESET`) even though the route itself is
 * healthy and responds correctly moments later — this is connection-pool/OS-socket pressure, not
 * an application defect. A genuine failure (a real 404/500, a route that is actually down) fails
 * identically on the retry, so this never masks a real regression; it only absorbs transient
 * connection-reset noise from the shared single-server topology.
 */
export async function getResilient(
  page: Page,
  url: string,
  options?: Parameters<Page["request"]["get"]>[1],
): Promise<APIResponse> {
  try {
    return await page.request.get(url, options);
  } catch {
    return await page.request.get(url, options);
  }
}
