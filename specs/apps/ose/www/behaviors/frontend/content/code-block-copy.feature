Feature: Code-Block Copy Button

  As a reader of the OSE platform site
  I want a copy-to-clipboard button on fenced code blocks
  So that I can copy example code without manually selecting it

  @unit
  Scenario: The renderer wraps a non-mermaid code figure in a CodeBlock
    Given the ose-www markdown renderer receives HTML with a non-mermaid code figure
    When the HTML is parsed to React
    Then the figure is wrapped in a CodeBlock exposing a copy button

  @unit
  Scenario: The renderer leaves a mermaid figure as a diagram
    Given the ose-www markdown renderer receives HTML with a mermaid code figure
    When the HTML is parsed to React
    Then the figure renders as a mermaid diagram with no copy button
