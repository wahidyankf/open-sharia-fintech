import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("service env reads", () => {
  const src = readFileSync(resolve(__dirname, "../../../../../src/features/content/shell/service.ts"), "utf-8");

  it("reads OSE_WEB_SHOW_DRAFTS via env object not process.env", () => {
    expect(src).toMatch(/env\.OSE_WEB_SHOW_DRAFTS/);
  });
});
