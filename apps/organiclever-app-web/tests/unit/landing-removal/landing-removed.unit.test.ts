import { existsSync } from "fs";
import path from "path";
import { describe, it, expect } from "vitest";

/**
 * Regression guard for the organiclever web split (Phase 6).
 *
 * The marketing `landing` experience moved to the dedicated `organiclever-www`
 * site. The app client (`organiclever-app-web`) must no longer carry a
 * `landing` context, and its root route must serve the app rather than the
 * marketing page.
 */
describe("landing context removal", () => {
  const appRoot = path.resolve(__dirname, "../../..");

  it("has no src/contexts/landing directory", () => {
    expect(existsSync(path.join(appRoot, "src/contexts/landing"))).toBe(false);
  });

  it("has no landing unit-test steps directory", () => {
    expect(existsSync(path.join(appRoot, "tests/unit/steps/landing"))).toBe(false);
  });
});
