import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const configSource = readFileSync(join(__dirname, "../../../next.config.ts"), "utf8");

describe("ayokoding-www locale redirects", () => {
  it("declares case-sensitive root and uppercase-locale redirects in Next config", () => {
    expect(configSource).toMatch(/experimental:\s*\{[\s\S]*?caseSensitiveRoutes:\s*true,/);
    expect(configSource).toContain('source: "/"');
    expect(configSource).toContain('destination: "/en"');

    for (const source of ["/EN", "/En", "/eN", "/ID", "/Id", "/iD"]) {
      expect(configSource).toContain(`source: "${source}"`);
    }
  });
});
