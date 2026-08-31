import { describe, it, expect } from "vitest";
import { renderCvPdf } from "./pdf";
import type { CvPdfDocumentModel } from "../core/pdf";

const document: CvPdfDocumentModel = {
  name: "Test Person",
  tagline: "Test Tagline",
  contactLine: "Email: test@example.com",
  summary: ["A summary paragraph."],
  experience: [
    {
      title: "Role",
      organization: "Org",
      period: "2020 - Present",
      details: ["Did the work."],
      meta: ["Skills: Testing"],
    },
  ],
  education: [],
  honors: [],
  languages: [{ name: "English", proficiency: "Native" }],
};

const collectPdfBuffer = (): Promise<Buffer> =>
  new Promise((resolve, reject) => {
    const pdf = renderCvPdf(document);
    const chunks: Buffer[] = [];
    pdf.on("data", (chunk) => chunks.push(chunk));
    pdf.on("end", () => resolve(Buffer.concat(chunks)));
    pdf.on("error", reject);
  });

describe("renderCvPdf", () => {
  it("produces a valid PDF byte stream", async () => {
    const buffer = await collectPdfBuffer();
    expect(buffer.subarray(0, 5).toString("ascii")).toBe("%PDF-");
    expect(buffer.length).toBeGreaterThan(0);
  });
});
