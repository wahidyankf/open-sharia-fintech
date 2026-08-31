import type { CVEntry } from "./data";

export type CvPdfSection = {
  title: string;
  organization: string;
  period: string;
  details: string[];
  meta: string[];
};

export type CvPdfLanguage = {
  name: string;
  proficiency: string;
};

export type CvPdfDocumentModel = {
  name: string;
  tagline: string;
  contactLine: string;
  summary: string[];
  experience: CvPdfSection[];
  education: CvPdfSection[];
  honors: CvPdfSection[];
  languages: CvPdfLanguage[];
};

const CONTACT_LABELS: Record<string, string> = {
  email: "Email",
  linkedin: "LinkedIn",
  website: "Website",
  github: "GitHub",
};

const toSection = (entry: CVEntry): CvPdfSection => ({
  title: entry.title,
  organization: entry.organization,
  period: entry.period,
  details: entry.details,
  meta: [
    entry.skills?.length ? `Skills: ${entry.skills.join(", ")}` : "",
    entry.programmingLanguages?.length ? `Programming Languages: ${entry.programmingLanguages.join(", ")}` : "",
    entry.frameworks?.length ? `Frameworks: ${entry.frameworks.join(", ")}` : "",
    entry.aiSkills?.length ? `AI Skills: ${entry.aiSkills.join(", ")}` : "",
  ].filter((line): line is string => line.length > 0),
});

const toLanguage = (detail: string): CvPdfLanguage => {
  const [name, proficiency] = detail.split("|");
  return { name: name ?? detail, proficiency: proficiency ?? "" };
};

export const buildCvPdfDocument = (data: CVEntry[]): CvPdfDocumentModel => {
  const about = data.find((entry) => entry.type === "about");
  const languageEntry = data.find((entry) => entry.type === "language");

  const contactLine = Object.entries(about?.links ?? {})
    .filter(([key]) => key in CONTACT_LABELS)
    .map(([key, value]) => `${CONTACT_LABELS[key]}: ${value}`)
    .join("   |   ");

  return {
    name: "Wahidyan Kresna Fridayoka",
    tagline: "Engineering Leader — Digital Banking, Fintech & RegTech",
    contactLine,
    summary: about?.details ?? [],
    experience: data.filter((entry) => entry.type === "work").map(toSection),
    education: data.filter((entry) => entry.type === "education").map(toSection),
    honors: data.filter((entry) => entry.type === "honor").map(toSection),
    languages: (languageEntry?.details ?? []).map(toLanguage),
  };
};
