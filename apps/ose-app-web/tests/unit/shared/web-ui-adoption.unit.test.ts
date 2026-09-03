/**
 * Phase 7d guard: ose-app-web is a canonical `@open-sharia-enterprise/web-ui`
 * consumer. At least one component must import a primitive from the design
 * system (the wiring also appears as a `web-ui` edge in the Nx graph and as an
 * `implicitDependencies` entry in project.json).
 *
 * The wiring already existed when Phase 7d ran, so this is a passing verify
 * rather than a red-first cycle.
 */
import { describe, it, expect } from "vitest";
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";

const WEB_UI_PACKAGE = "@open-sharia-enterprise/web-ui";

function collectSourceFiles(dir: string): string[] {
  const entries = readdirSync(dir, { withFileTypes: true });
  return entries.flatMap((entry) => {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) return collectSourceFiles(full);
    return /\.(ts|tsx)$/.test(entry.name) && !/\.unit\.test\.tsx?$/.test(entry.name) ? [full] : [];
  });
}

describe("ose-app-web web-ui adoption", () => {
  it("imports at least one primitive from @open-sharia-enterprise/web-ui", () => {
    const srcRoot = path.resolve(__dirname, "../../../src");
    const files = collectSourceFiles(srcRoot);
    const consumers = files.filter((file) => readFileSync(file, "utf8").includes(`from "${WEB_UI_PACKAGE}"`));
    expect(consumers.length).toBeGreaterThan(0);
  });

  it("uses the canonical package name (never a ts-ui alias)", () => {
    const srcRoot = path.resolve(__dirname, "../../../src");
    const files = collectSourceFiles(srcRoot);
    const tsUiUsages = files.filter((file) => readFileSync(file, "utf8").includes("@open-sharia-enterprise/ts-ui"));
    expect(tsUiUsages).toHaveLength(0);
  });
});
