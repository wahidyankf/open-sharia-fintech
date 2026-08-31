import React from "react";
import { render, screen, fireEvent } from "@testing-library/react";
import { describe, it, expect, vi, beforeEach } from "vitest";
import { HomeContent } from "@/features/home/shell/HomeContent";
import { filterItems } from "@/features/search/core/search";

// Mock the next/navigation module
const mockPush = vi.fn();
let mockSearchParams = new URLSearchParams();
vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: mockPush,
  }),
  useSearchParams: () => mockSearchParams,
}));

// Mock the components imported from other files
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

// Mock the filterItems function
vi.mock("@/features/search/core/search", () => ({
  filterItems: vi.fn((items) => items),
}));

// Mock the data and utility functions
vi.mock("@/features/cv/core/data", () => ({
  cvData: [
    {
      type: "about",
      details: ["Test about me"],
      links: {
        github: "https://github.com",
        linkedin: "https://linkedin.com",
        email: "test@example.com",
      },
    },
  ],
  getTopSkillsLastFiveYears: () => [
    { name: "Software Engineering", duration: 60 },
    { name: "Web Development", duration: 55 },
    { name: "React", duration: 50 },
  ],
  getTopLanguagesLastFiveYears: () => [
    { name: "JavaScript", duration: 60 },
    { name: "TypeScript", duration: 50 },
  ],
  getTopFrameworksLastFiveYears: () => [
    { name: "React", duration: 60 },
    { name: "Next.js", duration: 45 },
  ],
  getTopAISkillsLastFiveYears: () => [{ name: "AI-Agent Orchestration", duration: 10 }],
  formatDuration: (duration: number) => `${duration} months`,
}));

describe("Home component", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockSearchParams = new URLSearchParams();
    window.history.replaceState({}, "", "/");
  });

  it("renders the main sections", () => {
    render(<HomeContent />);
    expect(screen.getByText("Welcome to My Portfolio")).toBeInTheDocument();
    expect(screen.getByText("About Me")).toBeInTheDocument();
    expect(screen.getByText("Skills & Expertise")).toBeInTheDocument();
    expect(screen.getByText("Quick Links")).toBeInTheDocument();
    expect(screen.getByText("Connect With Me")).toBeInTheDocument();
  });

  it("renders the Navigation component", () => {
    render(<HomeContent />);
    expect(screen.getByTestId("navigation")).toBeInTheDocument();
  });

  it("renders the SearchComponent", () => {
    render(<HomeContent />);
    expect(screen.getByTestId("search-component")).toBeInTheDocument();
  });

  it("initializes search from the URL", () => {
    window.history.replaceState({}, "", "/?search=React");
    render(<HomeContent />);
    expect(screen.getByTestId("search-component")).toHaveValue("React");
  });

  it("renders the about me section", () => {
    render(<HomeContent />);
    expect(screen.getByText("Test about me")).toBeInTheDocument();
  });

  it("renders skills, languages, and frameworks", () => {
    render(<HomeContent />);
    expect(screen.getByText("Software Engineering")).toBeInTheDocument();
    expect(screen.getByText("JavaScript")).toBeInTheDocument();
    expect(screen.getAllByText("React")).toHaveLength(2);
  });

  it("renders quick links", () => {
    render(<HomeContent />);
    expect(screen.getByText("View My CV")).toBeInTheDocument();
    expect(screen.getByText("Browse My Personal Projects")).toBeInTheDocument();
  });

  it("renders connect with me links", () => {
    render(<HomeContent />);
    expect(screen.getByText("Github")).toBeInTheDocument();
    expect(screen.getByText("Linkedin")).toBeInTheDocument();
    expect(screen.getByText("Email")).toBeInTheDocument();
  });

  it("updates search term when typing in the search component", () => {
    render(<HomeContent />);
    const searchInput = screen.getByTestId("search-component") as HTMLInputElement;
    fireEvent.change(searchInput, { target: { value: "React" } });
    expect(searchInput.value).toBe("React");
  });

  it("filters content based on search term", () => {
    render(<HomeContent />);
    const searchInput = screen.getByTestId("search-component");
    fireEvent.change(searchInput, { target: { value: "React" } });

    expect(filterItems).toHaveBeenCalled();
  });

  it("handles item click and navigates to CV page", () => {
    render(<HomeContent />);
    const skillButtons = screen.getAllByText("React");
    fireEvent.click(skillButtons[0]);
    expect(mockPush).toHaveBeenCalledWith("/cv?search=React&scrollTop=true");
  });

  it("handles language button click and navigates to CV page", () => {
    render(<HomeContent />);
    const languageButton = screen.getByText("JavaScript");
    fireEvent.click(languageButton);
    expect(mockPush).toHaveBeenCalledWith("/cv?search=JavaScript&scrollTop=true");
  });

  it("handles framework button click and navigates to CV page", () => {
    render(<HomeContent />);
    const frameworkButton = screen.getByText("Next.js");
    fireEvent.click(frameworkButton);
    expect(mockPush).toHaveBeenCalledWith("/cv?search=Next.js&scrollTop=true");
  });

  it("updates URL when typing in search", () => {
    render(<HomeContent />);
    const searchInput = screen.getByTestId("search-component") as HTMLInputElement;
    fireEvent.change(searchInput, { target: { value: "TypeScript" } });
    expect(mockPush).toHaveBeenCalledWith("/?search=TypeScript", { scroll: false });
  });

  it("handles TypeScript skill pill click navigates with scrollTop", () => {
    render(<HomeContent />);
    const languageButton = screen.getByText("TypeScript");
    fireEvent.click(languageButton);
    expect(mockPush).toHaveBeenCalledWith("/cv?search=TypeScript&scrollTop=true");
  });
});
