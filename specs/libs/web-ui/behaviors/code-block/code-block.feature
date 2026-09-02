Feature: CodeBlock primitive

  A layout composer that overlays a CopyButton on an already-highlighted code figure, establishing
  its own positioning context and copying the verbatim multi-line source.

  @unit
  Scenario: The code block renders its highlighted children and a copy button
    Given a CodeBlock rendered with code text and a highlighted <pre> child
    When the component mounts
    Then the highlighted child is present
    And a copy button is present within the code-block wrapper

  @unit
  Scenario: Copying from the code block yields the verbatim multi-line source
    Given a CodeBlock whose code prop is a three-line annotated snippet with trailing comments
    When the user clicks the code block's copy button
    Then the clipboard receives the snippet byte-for-byte including every annotation and newline

  @unit
  Scenario: The code block establishes its own positioning context
    Given a CodeBlock is rendered
    When its wrapper is inspected
    Then the wrapper is a relatively-positioned element carrying data-slot "code-block"

  @unit
  Scenario: The copy button stays pinned outside the code's horizontal-scroll region
    Given a CodeBlock rendered with a highlighted <pre> child
    When the copy button's position in the DOM is inspected
    Then the copy button is a child of the wrapper, not a descendant of the scrolling <pre>

  @unit
  Scenario: The copy button is discoverable at rest and reveals fully on hover or focus
    Given a CodeBlock is rendered
    When the copy button's resting presentation is inspected
    Then the copy button is partially visible at rest rather than fully hidden
    And it becomes fully visible on hover, focus, and touch

  @unit
  Scenario: The code block reserves scroll-margin so its copy button clears a sticky header
    Given a CodeBlock is rendered
    When the wrapper is inspected
    Then the wrapper reserves top scroll-margin

  @visual
  Scenario: The code block renders correctly in light and dark themes
    Given the CodeBlock stories are loaded in Storybook
    When the resting and copied stories are captured in light and dark themes
    Then each screenshot matches its committed visual baseline
