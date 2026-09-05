import { afterEach, beforeEach, describe, expect, it } from "vitest";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { processAllIndexFiles } from "../../../../../src/features/content/shell/index-generator";

describe("processAllIndexFiles", () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "index-generator-test-"));
  });

  afterEach(async () => {
    await fs.rm(tmpDir, { recursive: true, force: true });
  });

  async function writeFile(relPath: string, content: string): Promise<string> {
    const fullPath = path.join(tmpDir, relPath);
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    await fs.writeFile(fullPath, content, "utf-8");
    return fullPath;
  }

  it("regenerates a section's body as a child-link list when it has children", async () => {
    await writeFile(
      "en/parent/_index.md",
      '---\ntitle: "Parent"\ndate: 2026-01-01T00:00:00+07:00\ndraft: false\nweight: 1\n---\n',
    );
    await writeFile(
      "en/parent/child/_index.md",
      '---\ntitle: "Child"\ndate: 2026-01-01T00:00:00+07:00\ndraft: false\nweight: 1\n---\n',
    );

    const result = await processAllIndexFiles(tmpDir, "generate");

    expect(result.errors).toEqual([]);
    const parentContent = await fs.readFile(path.join(tmpDir, "en/parent/_index.md"), "utf-8");
    expect(parentContent).toContain("- [Child](/en/parent/child)");
  });

  it("does NOT wipe a childless section's hand-authored body (regression: e2e-fixture-alpha/_index.md data loss)", async () => {
    const authoredBody =
      "This ramp starts with the shell and version control, because the alpha fixture assumes zero prior command-line exposure.";
    const filePath = await writeFile(
      "en/leaf/_index.md",
      `---\ntitle: "Leaf"\ndate: 2026-01-01T00:00:00+07:00\ndraft: false\nweight: 1\n---\n\n${authoredBody}\n`,
    );

    const result = await processAllIndexFiles(tmpDir, "generate");

    expect(result.errors).toEqual([]);
    const afterContent = await fs.readFile(filePath, "utf-8");
    expect(afterContent).toContain(authoredBody);
  });

  it("still adds missing frontmatter fields (date/draft) to a childless section without touching its body", async () => {
    const authoredBody = "Hand-authored body text that must survive.";
    const filePath = await writeFile("en/leaf/_index.md", `---\ntitle: "Leaf"\n---\n\n${authoredBody}\n`);

    const result = await processAllIndexFiles(tmpDir, "generate");

    expect(result.errors).toEqual([]);
    const afterContent = await fs.readFile(filePath, "utf-8");
    expect(afterContent).toContain("date:");
    expect(afterContent).toContain("draft: false");
    expect(afterContent).toContain(authoredBody);
  });

  it("validate mode reports a childless section as unchanged when only its body is hand-authored", async () => {
    await writeFile(
      "en/leaf/_index.md",
      '---\ntitle: "Leaf"\ndate: 2026-01-01T00:00:00+07:00\ndraft: false\nweight: 1\n---\n\nHand-authored body.\n',
    );

    const result = await processAllIndexFiles(tmpDir, "validate");

    expect(result.errors).toEqual([]);
    expect(result.changed).toEqual([]);
  });
});
