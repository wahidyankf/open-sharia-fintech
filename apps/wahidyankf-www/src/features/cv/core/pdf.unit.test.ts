import { describe, it, expect } from "vitest";
import { buildCvPdfDocument } from "./pdf";
import type { CVEntry } from "./data";

const fixture: CVEntry[] = [
  {
    type: "about",
    title: "About Me",
    organization: "",
    period: "",
    details: ["Summary paragraph one.", "Summary paragraph two."],
    links: {
      github: "https://github.com/example",
      linkedin: "https://linkedin.com/in/example",
      website: "https://example.com",
      email: "example@example.com",
      credential: "https://example.com/credential",
    },
  },
  {
    type: "work",
    title: "Software Engineer",
    organization: "Example Co",
    period: "January 2020 - Present",
    details: ["Did engineering work."],
    skills: ["Leadership"],
    programmingLanguages: ["TypeScript"],
    frameworks: ["Next.js"],
    aiSkills: ["AI-augmented SDLC"],
  },
  {
    type: "education",
    title: "B.Eng.",
    organization: "Example University",
    period: "2010 - 2014",
    details: ["Field of study: Engineering"],
  },
  {
    type: "certification",
    title: "Example Certification",
    organization: "Example Institute",
    period: "June 2021",
    details: ["Credential ID: abc123"],
  },
  {
    type: "honor",
    title: "Example Award",
    organization: "Example Institute",
    period: "October 2021",
    details: ["Associated with: Example role"],
  },
  {
    type: "language",
    title: "Languages",
    organization: "",
    period: "",
    details: ["English|Full professional proficiency", "French|Elementary proficiency"],
  },
];

describe("buildCvPdfDocument", () => {
  it("carries the fixed name and tagline used across the site's metadata", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.name).toBe("Wahidyan Kresna Fridayoka");
    expect(doc.tagline).toBe("Engineering Leader — Digital Banking, Fintech & RegTech");
  });

  it("builds the contact line from the about entry's known links only", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.contactLine).toBe(
      "GitHub: https://github.com/example   |   LinkedIn: https://linkedin.com/in/example   |   Website: https://example.com   |   Email: example@example.com",
    );
  });

  it("pulls the about entry's details into the summary", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.summary).toEqual(["Summary paragraph one.", "Summary paragraph two."]);
  });

  it("shapes work entries into experience sections with joined meta lines", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.experience).toEqual([
      {
        title: "Software Engineer",
        organization: "Example Co",
        period: "January 2020 - Present",
        details: ["Did engineering work."],
        meta: [
          "Skills: Leadership",
          "Programming Languages: TypeScript",
          "Frameworks: Next.js",
          "AI Skills: AI-augmented SDLC",
        ],
      },
    ]);
  });

  it("omits meta lines for fields the entry does not have", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.education).toEqual([
      {
        title: "B.Eng.",
        organization: "Example University",
        period: "2010 - 2014",
        details: ["Field of study: Engineering"],
        meta: [],
      },
    ]);
    expect(doc.honors).toEqual([
      {
        title: "Example Award",
        organization: "Example Institute",
        period: "October 2021",
        details: ["Associated with: Example role"],
        meta: [],
      },
    ]);
  });

  it("does not surface certification entries in the PDF model", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc).not.toHaveProperty("certifications");
  });

  it("splits the pipe-delimited language entry into name/proficiency pairs", () => {
    const doc = buildCvPdfDocument(fixture);
    expect(doc.languages).toEqual([
      { name: "English", proficiency: "Full professional proficiency" },
      { name: "French", proficiency: "Elementary proficiency" },
    ]);
  });

  it("returns empty collections when the about or language entries are absent", () => {
    const workOnly = fixture.filter((entry) => entry.type === "work");
    const doc = buildCvPdfDocument(workOnly);
    expect(doc.contactLine).toBe("");
    expect(doc.summary).toEqual([]);
    expect(doc.languages).toEqual([]);
  });
});
