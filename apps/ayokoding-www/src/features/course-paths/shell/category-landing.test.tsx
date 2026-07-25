import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PathManifest } from "../core/schemas";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { CategoryLanding } from "./category-landing";

afterEach(cleanup);

function manifest(overrides: Partial<PathManifest> & Pick<PathManifest, "pathId" | "arc">): PathManifest {
  return {
    title: overrides.pathId,
    description: "desc",
    courseOrder: [],
    ...overrides,
  };
}

describe("CategoryLanding — careers instance (Cycle 3.1b-i, R7)", () => {
  const interviewReady = manifest({ pathId: "careers/interview-ready/role-a", arc: "interview-ready" });
  const immediatelyA = manifest({ pathId: "careers/immediately-effective/role-b", arc: "immediately-effective" });
  const immediatelyB = manifest({ pathId: "careers/immediately-effective/role-c", arc: "immediately-effective" });

  it("renders one ArcCard per arc, member roles previewed", () => {
    render(<CategoryLanding locale="en" category="careers" manifests={[interviewReady, immediatelyA, immediatelyB]} />);

    const nav = within(screen.getByRole("navigation", { name: "Careers arcs" }));
    const links = nav.getAllByRole("link");
    expect(links.length).toBe(2);
  });

  it("the immediately-effective arc card previews exactly two member roles", () => {
    render(<CategoryLanding locale="en" category="careers" manifests={[interviewReady, immediatelyA, immediatelyB]} />);

    const card = screen.getByRole("link", { name: /immediately-effective/i });
    expect(within(card).getAllByRole("listitem").length).toBe(2);
  });

  it("renders the shared empty state when no careers manifest is loaded", () => {
    render(<CategoryLanding locale="en" category="careers" manifests={[]} />);

    expect(screen.getByRole("alert")).toBeTruthy();
    expect(screen.queryByRole("navigation", { name: "Careers arcs" })).toBeNull();
  });
});

describe("CategoryLanding — skills instance (Cycle 3.1b-ii, R7/R8)", () => {
  const subjectA = manifest({ pathId: "skills/subject-a", arc: "track-a", title: "Subject A" });
  const subjectB = manifest({ pathId: "skills/subject-b", arc: "track-b", title: "Subject B" });

  it("states the fixed-arc ramp promise once, with no arc-selection control anywhere", () => {
    render(<CategoryLanding locale="en" category="skills" manifests={[subjectA, subjectB]} />);

    expect(screen.queryByRole("navigation", { name: "Careers arcs" })).toBeNull();
    expect(screen.queryByRole("combobox")).toBeNull();
    expect(screen.queryByRole("radiogroup")).toBeNull();
  });

  it("renders the shared PathCard hub grid for the subject manifests", () => {
    render(<CategoryLanding locale="en" category="skills" manifests={[subjectA, subjectB]} />);

    const nav = within(screen.getByRole("navigation", { name: "Skills paths" }));
    expect(nav.getAllByRole("link").length).toBe(2);
  });

  it("renders the shared empty state when no skills manifest is loaded", () => {
    render(<CategoryLanding locale="en" category="skills" manifests={[]} />);

    expect(screen.getByRole("alert")).toBeTruthy();
  });
});
