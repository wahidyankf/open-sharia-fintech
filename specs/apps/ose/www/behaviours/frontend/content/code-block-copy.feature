Feature: Code-Block Copy Button

  As a reader of the OSE platform site
  I want a copy-to-clipboard button on fenced code blocks
  So that I can copy example code without manually selecting it

  # Exemption(e2e): the public browser boundary cannot inject the renderer's private pre-parsed HTML input while isolating this transformation; alternative-proof: ose-www:test:unit / The renderer wraps a non-mermaid code figure in a CodeBlock
  @e2e-exempt
  # Exemption(integration): the renderer transformation is in-process and owns no local resource boundary; alternative-proof: ose-www:test:unit / The renderer wraps a non-mermaid code figure in a CodeBlock
  @integration-exempt
  Scenario: The renderer wraps a non-mermaid code figure in a CodeBlock
    Given the ose-www markdown renderer receives HTML with a non-mermaid code figure
    When the HTML is parsed to React
    Then the figure is wrapped in a CodeBlock exposing a copy button

  # Exemption(e2e): the public browser boundary cannot inject the renderer's private pre-parsed Mermaid HTML input while isolating this transformation; alternative-proof: ose-www:test:unit / The renderer leaves a mermaid figure as a diagram
  @e2e-exempt
  # Exemption(integration): the renderer transformation is in-process and owns no local resource boundary; alternative-proof: ose-www:test:unit / The renderer leaves a mermaid figure as a diagram
  @integration-exempt
  Scenario: The renderer leaves a mermaid figure as a diagram
    Given the ose-www markdown renderer receives HTML with a mermaid code figure
    When the HTML is parsed to React
    Then the figure renders as a mermaid diagram with no copy button
