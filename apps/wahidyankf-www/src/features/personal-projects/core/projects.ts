import { filterItems } from "@/features/search/core/search";

export type Project = {
  title: string;
  description: string;
  details: string[];
  links: {
    [key: string]: string;
  };
};

export const projects: Project[] = [
  {
    title: "Open Sharia Enterprise (OSE)",
    description:
      "A pre-alpha, open-source platform for researching and building trustworthy, Sharia-compliant enterprise products, built in public. Current work spans the OrganicLever productivity-tracker foundation, AyoKoding engineering research and learning, and reusable governance and quality automation across a polyglot Nx monorepo.",
    details: [
      "Enforces quality through Gherkin-driven spec coverage and three-level testing (unit, integration, E2E)",
      "AI-agent-orchestrated development workflow across the monorepo",
      "MIT licensed — fully open-source across all apps and libs",
    ],
    links: {
      repository: "https://github.com/wahidyankf/ose-public",
      website: "https://oseplatform.com/",
    },
  },
  {
    title: "BeaverNest",
    description:
      "A privately hosted Phoenix LiveView family assistant for local Codex sessions, with role-gated repository access and test-backed safety controls.",
    details: [
      "Chat is read-only by default; explicit role-gated repository writes are opt-in",
      "Safeguards for accounts with the children role",
      "Session-reset safety",
      "Covered by unit, integration, and browser tests",
    ],
    links: {
      repository: "https://github.com/wahidyankf/beaver-nest",
    },
  },
  {
    title: "AyoKoding",
    description:
      "A free educational platform for software engineering, featuring a blog and YouTube channel. Created to learn in public and give back to the community.",
    details: [
      "Comprehensive learning resources for software engineering",
      "Public learning platform to share knowledge",
      "Includes a YouTube channel for video content",
    ],
    links: {
      repository: "https://github.com/organiclever/ayokoding",
      website: "https://ayokoding.com/",
      YouTube: "https://www.youtube.com/@AyoKoding",
    },
  },
  {
    title: "OrganicLever",
    description: "A web application focused on team and personal productivity (in progress).",
    details: [
      "Aims to improve team collaboration",
      "Enhances personal productivity",
      "Web-based application for easy access",
    ],
    links: {
      website: "https://www.organiclever.com/",
    },
  },
];

export type ProjectFilter = string;

export function filterProjects(projects: Project[], filter: ProjectFilter): Project[] {
  return filterItems(projects, filter, ["title", "description", "details"]);
}
