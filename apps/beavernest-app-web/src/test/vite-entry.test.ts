import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const appRoot = resolve(import.meta.dirname, "../..");

describe("Vite application entry", () => {
  it("provides the static CSR entry and Vite build surface", () => {
    expect(existsSync(resolve(appRoot, "index.html"))).toBe(true);
    expect(existsSync(resolve(appRoot, "vite.config.ts"))).toBe(true);
    expect(existsSync(resolve(appRoot, "src/main.tsx"))).toBe(true);
    expect(readFileSync(resolve(appRoot, "project.json"), "utf8")).toContain("platform:vite");
  });
});
