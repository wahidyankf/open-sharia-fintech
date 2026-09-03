import { readdirSync, readFileSync, statSync } from "fs";
import path from "path";
import { describe, it, expect } from "vitest";

/**
 * Verifies that organiclever-app-web consumes the shared design system
 * (`@open-sharia-enterprise/web-ui`) from at least one component, and that
 * every web-ui import uses the canonical package name (decision #26 — web-ui,
 * not ts-ui).
 */
const CANONICAL = "@open-sharia-enterprise/web-ui";
const srcRoot = path.resolve(__dirname, "../../../src");

function collectTsxFiles(dir: string): string[] {
  const out: string[] = [];
  for (const entry of readdirSync(dir)) {
    const full = path.join(dir, entry);
    if (statSync(full).isDirectory()) {
      out.push(...collectTsxFiles(full));
    } else if (full.endsWith(".tsx") || full.endsWith(".ts")) {
      out.push(full);
    }
  }
  return out;
}

describe("web-ui design-system consumption", () => {
  const files = collectTsxFiles(srcRoot);

  it("imports @open-sharia-enterprise/web-ui in at least one component", () => {
    const consumers = files.filter((f) => {
      const content = readFileSync(f, "utf8");
      return new RegExp(`from ["']${CANONICAL}["']`).test(content);
    });
    expect(consumers.length).toBeGreaterThan(0);
  });

  it("uses only the canonical web-ui package name (never a ts-ui alias)", () => {
    const offenders = files.filter((f) => {
      const content = readFileSync(f, "utf8");
      return /@open-sharia-enterprise\/ts-ui/.test(content);
    });
    expect(offenders).toEqual([]);
  });
});
