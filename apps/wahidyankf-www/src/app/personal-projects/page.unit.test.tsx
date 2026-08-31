import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { PersonalProjectsContent } from "@/features/personal-projects/shell/PersonalProjectsContent";

// Mock declarations
const mockPush = vi.fn();
let mockSearchParams = new URLSearchParams();

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  useSearchParams: () => mockSearchParams,
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => <div data-testid="navigation">Navigation</div>,
}));

vi.mock("@open-sharia-enterprise/web-ui", () => ({
  SearchComponent: ({
    searchTerm,
    setSearchTerm,
    updateURL,
    placeholder,
  }: {
    searchTerm: string;
    setSearchTerm: (term: string) => void;
    updateURL: (term: string) => void;
    placeholder: string;
  }) => (
    <input
      data-testid="search-component"
      value={searchTerm}
      onChange={(e) => {
        setSearchTerm(e.target.value);
        updateURL(e.target.value);
      }}
      placeholder={placeholder}
    />
  ),
  HighlightText: ({ text }: { text: string }) => <span>{text}</span>,
}));

// Define a type for the project items
type ProjectItem = {
  title: string;
  description: string;
  details: string[];
  links: Record<string, string>;
};

vi.mock("@/features/search/core/search", () => ({
  filterItems: vi.fn((items: ProjectItem[], searchTerm: string) =>
    items.filter((item) => item.title.toLowerCase().includes(searchTerm.toLowerCase())),
  ),
}));

describe("Personal Projects component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSearchParams = new URLSearchParams();
    window.history.replaceState({}, "", "/personal-projects");
  });

  it("renders the main sections", () => {
    render(<PersonalProjectsContent />);
    expect(screen.getByText("Personal Projects")).toBeInTheDocument();
    expect(screen.getByTestId("search-component")).toBeInTheDocument();
    expect(screen.getByTestId("navigation")).toBeInTheDocument();
  });

  it("renders all projects initially", () => {
    render(<PersonalProjectsContent />);
    expect(screen.getByText("Open Sharia Enterprise (OSE)")).toBeInTheDocument();
    expect(screen.getByText("BeaverNest")).toBeInTheDocument();
    expect(screen.getByText("AyoKoding")).toBeInTheDocument();
    expect(screen.getByText("OrganicLever")).toBeInTheDocument();
  });

  it("initializes search from the URL", () => {
    window.history.replaceState({}, "", "/personal-projects?search=AyoKoding");
    render(<PersonalProjectsContent />);
    expect(screen.getByTestId("search-component")).toHaveValue("AyoKoding");
    expect(screen.getByText("AyoKoding")).toBeInTheDocument();
    expect(screen.queryByText("OrganicLever")).not.toBeInTheDocument();
  });

  it("filters projects based on search term", async () => {
    render(<PersonalProjectsContent />);
    const searchInput = screen.getByTestId("search-component");
    fireEvent.change(searchInput, { target: { value: "AyoKoding" } });

    await waitFor(() => {
      expect(screen.getByText("AyoKoding")).toBeInTheDocument();
      expect(screen.queryByText("OrganicLever")).not.toBeInTheDocument();
    });
  });

  it("displays 'No projects found' message when no matches", async () => {
    render(<PersonalProjectsContent />);
    const searchInput = screen.getByTestId("search-component");
    fireEvent.change(searchInput, { target: { value: "NonexistentProject" } });

    await waitFor(() => {
      expect(screen.getByText("No projects found matching your search.")).toBeInTheDocument();
    });
  });

  it("updates URL when searching", async () => {
    render(<PersonalProjectsContent />);
    const searchInput = screen.getByTestId("search-component");
    fireEvent.change(searchInput, { target: { value: "AyoKoding" } });

    await waitFor(() => {
      expect(mockPush).toHaveBeenCalledWith("/personal-projects?search=AyoKoding", { scroll: false });
    });
  });

  it("renders project links correctly", () => {
    render(<PersonalProjectsContent />);

    const repositoryLinks = screen.getAllByRole("link", {
      name: /Repository/i,
    });
    expect(repositoryLinks[0]).toHaveAttribute("href", "https://github.com/wahidyankf/ose-public");
    expect(repositoryLinks[1]).toHaveAttribute("href", "https://github.com/wahidyankf/beaver-nest");
    expect(repositoryLinks[2]).toHaveAttribute("href", "https://github.com/organiclever/ayokoding");

    const websiteLinks = screen.getAllByRole("link", { name: /Website/i });
    expect(websiteLinks[0]).toHaveAttribute("href", "https://oseplatform.com/");
    expect(websiteLinks[1]).toHaveAttribute("href", "https://ayokoding.com/");

    const youtubeLink = screen.getByRole("link", { name: /YouTube/i });
    expect(youtubeLink).toHaveAttribute("href", "https://www.youtube.com/@AyoKoding");
  });
});
