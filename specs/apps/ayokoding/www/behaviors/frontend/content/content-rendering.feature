Feature: Content Rendering

  As a reader visiting AyoKoding
  I want page content to render correctly with all supported formats
  So that I can read articles, code, diagrams, and interactive elements as intended

  Background:
    Given the app is running

  @unit @e2e
  Scenario: Markdown prose renders with proper formatting classes
    When a visitor opens a content page with prose body text
    Then the body text should have prose typography classes applied
    And headings should be visually distinct from body text
    And paragraph spacing should be consistent

  @unit @e2e
  Scenario: Code blocks render with syntax highlighting via Shiki
    When a visitor opens a content page containing a fenced code block
    Then the code block should display with syntax-highlighted tokens
    And the language label should be shown above the code block
    And the block should use a monospace font

  @unit @e2e
  Scenario: Callout shortcode renders as an Alert admonition
    When a visitor opens a content page containing a callout shortcode
    Then the callout should render as an admonition block
    And the admonition should display the appropriate icon and label for its type
    And the callout body text should be visible inside the admonition

  @unit @e2e
  Scenario: Tabs shortcode renders as tabbed panels
    When a visitor opens a content page containing a tabs shortcode
    Then the tabs should render as a tab bar with clickable tab labels
    And the visitor clicks a tab label
    And the corresponding panel content should become visible
    And the other panels should be hidden

  @unit @e2e
  Scenario: YouTube shortcode renders as a responsive iframe embed
    When a visitor opens a content page containing a YouTube shortcode
    Then a responsive iframe embed should be visible
    And the iframe src should point to the YouTube embed URL
    And the embed should maintain a 16:9 aspect ratio

  @unit @e2e
  Scenario: Steps shortcode renders as a numbered step list
    When a visitor opens a content page containing a steps shortcode
    Then the steps should render as an ordered list of numbered items
    And each step should display its number prominently
    And the step content should be indented beneath its number

  @unit @e2e
  Scenario: Inline math expression renders via KaTeX
    When a visitor opens a content page containing an inline math expression delimited by $...$
    Then the expression should render as formatted math notation inline with surrounding text
    And the rendered math should not display raw LaTeX source

  @unit @e2e
  Scenario: Block math expression renders via KaTeX
    When a visitor opens a content page containing a block math expression delimited by $$...$$
    Then the expression should render as a centered display math block
    And the rendered math should not display raw LaTeX source

  @unit @e2e
  Scenario: Mermaid diagram renders as an SVG
    When a visitor opens a content page containing a Mermaid code block
    Then the diagram should render as an inline SVG element
    And the raw Mermaid source should not be visible to the visitor

  @unit @e2e
  Scenario: Raw HTML inline elements render correctly
    When a visitor opens a content page containing raw HTML such as inline div, table, and details elements
    Then the HTML elements should render in the browser as expected
    And the elements should be visible and styled appropriately
