import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("repository-fs env reads", () => {
  const src = readFileSync(resolve(__dirname, "../../../../../src/features/content/shell/repository-fs.ts"), "utf-8");

  it("reads OSE_WEB_CONTENT_DIR via env object not process.env", () => {
    expect(src).toMatch(/env\.OSE_WEB_CONTENT_DIR/);
  });

  it("reads OSE_WEB_SHOW_DRAFTS via env object not process.env", () => {
    expect(src).toMatch(/env\.OSE_WEB_SHOW_DRAFTS/);
  });
});
