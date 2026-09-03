import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("next.config.ts env.ts import", () => {
  it("next.config.ts imports ./src/env.ts for build-time validation", () => {
    const configPath = resolve(__dirname, "../../next.config.ts");
    const content = readFileSync(configPath, "utf-8");
    expect(content).toMatch(/import\s+["']\.\/src\/env/);
  });
});
