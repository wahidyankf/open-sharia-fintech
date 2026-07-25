import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { SyllabusPreview } from "./syllabus-preview";

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
});
