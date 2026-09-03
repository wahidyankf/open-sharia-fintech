import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { SyllabusPreview } from "../../../../../src/features/course-paths/shell/syllabus-preview";

afterEach(cleanup);

describe("SyllabusPreview (Cycle 3.1c-ii — arc landing single-role inline preview, R7)", () => {
  it("renders a real <ol> so 'number is order' semantics carry over from path-landing's syllabus", () => {
    render(
      <SyllabusPreview
        courseTitles={["Just Enough Python", "Just Enough Bash", "Version Control & Git", "Data Structures"]}
      />,
    );

    const list = screen.getByRole("list");
    expect(list.tagName).toBe("OL");
  });

  it("shows only the first phase's courses (capped at 3), never the whole manifest", () => {
    render(
      <SyllabusPreview
        courseTitles={["Just Enough Python", "Just Enough Bash", "Version Control & Git", "Data Structures"]}
      />,
    );

    const items = screen.getAllByRole("listitem");
    expect(items.length).toBe(3);
    expect(screen.queryByText("Data Structures")).toBeNull();
  });

  it("renders a 'Starts with:' label", () => {
    render(<SyllabusPreview courseTitles={["Just Enough Python"]} />);

    expect(screen.getByText(/Starts with:/i)).toBeTruthy();
  });

  it("renders each course title with no manually-added list-index prefix (DWT-002 fix, phase-5 rule-15 design-tester retest)", () => {
    // Real course titles already embed their own catalog number (e.g. "4 · Just Enough Python");
    // a second, locally-rendered "1." in front of it produced a nonsensical double-number.
    render(<SyllabusPreview courseTitles={["4 · Just Enough Python", "7 · Data Structures & Algorithms"]} />);

    const items = screen.getAllByRole("listitem");
    expect(items[0]?.textContent).toBe("4 · Just Enough Python");
    expect(items[1]?.textContent).toBe(" · 7 · Data Structures & Algorithms");
    expect(screen.queryByText(/^1\.\s*4/)).toBeNull();
  });

  it("never nests the <ol> inside a <p> — invalid HTML that triggers a hydration mismatch (phase-5 EWT finding)", () => {
    // <p> only permits phrasing content per the HTML spec; a block-level <ol> descendant is
    // invalid nesting. Browsers silently close the <p> early to recover, so SSR output and the
    // hydrated client tree diverge, and React logs "In HTML, <ol> cannot be a descendant of <p>"
    // plus a hydration-mismatch error at every arc-landing single-role render (caught live via
    // Playwright MCP at http://localhost:3101/en/learn/paths/careers/interview-ready).
    const { container } = render(<SyllabusPreview courseTitles={["Just Enough Python"]} />);

    const list = screen.getByRole("list");
    expect(list.closest("p")).toBeNull();

    const paragraphs = container.querySelectorAll("p");
    for (const paragraph of paragraphs) {
      expect(paragraph.querySelector("ol, ul, div, table, section, article")).toBeNull();
    }
  });
});
