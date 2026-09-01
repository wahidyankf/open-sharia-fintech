/**
 * Structure guard: `src/features/` is the module root for ose-www (the same
 * shape organiclever-www uses), each feature splits into a functional `core/` (pure)
 * and an imperative `shell/` (IO + UI + wiring), and the tRPC content/feed
 * pipeline remains reachable through the new layout.
 *
 * RED: fails before the contexts -> features reshape (import paths unresolved).
 * GREEN: passes once src/features/ exists, the core/shell split is in place,
 * and the tRPC router/feed builder resolve from it.
 */
import { describe, it, expect } from "vitest";
import { existsSync } from "node:fs";
import path from "node:path";

describe("ose-www features module root", () => {
  it("exposes src/features/ as the module root (contexts/ removed)", () => {
    const root = path.resolve(__dirname, "../../../src");
    expect(existsSync(path.join(root, "features"))).toBe(true);
    expect(existsSync(path.join(root, "contexts"))).toBe(false);
  });

  it("splits each feature into core/ (pure) and shell/ (IO + UI)", () => {
    const features = path.resolve(__dirname, "../../../src/features");
    // content carries both layers: pure derivations in core/, IO + UI in shell/.
    expect(existsSync(path.join(features, "content/core/reader.ts"))).toBe(true);
    expect(existsSync(path.join(features, "content/shell/service.ts"))).toBe(true);
    // legacy DDD layer folders are gone.
    expect(existsSync(path.join(features, "content/application"))).toBe(false);
    expect(existsSync(path.join(features, "content/infrastructure"))).toBe(false);
    expect(existsSync(path.join(features, "content/presentation"))).toBe(false);
  });

  it("keeps the tRPC app router reachable from features/", async () => {
    const mod = await import("@/features/app-shell/shell/root-router");
    expect(mod.appRouter).toBeDefined();
  }, 30_000);

  it("keeps the content service (feed source) reachable from features/", async () => {
    const mod = await import("@/features/content/shell/service");
    expect(mod.ContentService).toBeDefined();
  });

  it("keeps the rss feed builder under features/ (server-only module)", () => {
    // feed-builder pulls the Next.js `server-only` tRPC server caller, so it is
    // asserted by file location rather than imported into the node test env.
    const root = path.resolve(__dirname, "../../../src");
    expect(existsSync(path.join(root, "features/rss-feed/shell/feed-builder.ts"))).toBe(true);
  });
});
