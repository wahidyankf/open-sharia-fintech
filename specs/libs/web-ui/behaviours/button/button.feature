Feature: Button component

  As a developer using the web-ui design system
  I want the Button component to render correctly with all variants, sizes, and states
  So that I can build accessible and consistent user interfaces

  Scenario: Renders with default variant and size
    When the Button is rendered with label "Click me"
    Then the button element should be present in the document
    And the button should have data-variant "default"
    And the button should have data-size "default"

  Scenario: Renders variant default
    When the Button is rendered with variant "default" and label "default"
    Then the button element with label "default" should be present

  Scenario: Renders variant destructive
    When the Button is rendered with variant "destructive" and label "destructive"
    Then the button element with label "destructive" should be present

  Scenario: Renders variant outline
    When the Button is rendered with variant "outline" and label "outline"
    Then the button element with label "outline" should be present

  Scenario: Renders variant secondary
    When the Button is rendered with variant "secondary" and label "secondary"
    Then the button element with label "secondary" should be present

  Scenario: Renders variant ghost
    When the Button is rendered with variant "ghost" and label "ghost"
    Then the button element with label "ghost" should be present

  Scenario: Renders variant link
    When the Button is rendered with variant "link" and label "link"
    Then the button element with label "link" should be present

  Scenario: Renders size default
    When the Button is rendered with size "default" and aria-label "button-default"
    Then the button element with aria-label "button-default" should be present

  Scenario: Renders size xs
    When the Button is rendered with size "xs" and aria-label "button-xs"
    Then the button element with aria-label "button-xs" should be present

  Scenario: Renders size sm
    When the Button is rendered with size "sm" and aria-label "button-sm"
    Then the button element with aria-label "button-sm" should be present

  Scenario: Renders size lg
    When the Button is rendered with size "lg" and aria-label "button-lg"
    Then the button element with aria-label "button-lg" should be present

  Scenario: Renders size icon
    When the Button is rendered with size "icon" and aria-label "button-icon"
    Then the button element with aria-label "button-icon" should be present

  Scenario: Renders size icon-xs
    When the Button is rendered with size "icon-xs" and aria-label "button-icon-xs"
    Then the button element with aria-label "button-icon-xs" should be present

  Scenario: Renders size icon-sm
    When the Button is rendered with size "icon-sm" and aria-label "button-icon-sm"
    Then the button element with aria-label "button-icon-sm" should be present

  Scenario: Renders size icon-lg
    When the Button is rendered with size "icon-lg" and aria-label "button-icon-lg"
    Then the button element with aria-label "button-icon-lg" should be present

  Scenario: Supports disabled state
    When the Button is rendered as disabled with label "Disabled"
    Then the button element should have the disabled attribute

  Scenario: Renders as child element when asChild is true
    When the Button is rendered with asChild wrapping an anchor to "/test" with label "Link Button"
    Then a link element with label "Link Button" should be present
    And the link should have href "/test"

  Scenario: Has no accessibility violations
    When the Button is rendered with label "Accessible Button"
    Then the button should have no accessibility violations

  Scenario: Renders variant teal
    When I render a Button with variant "teal"
    Then the button should have data-variant "teal"

  Scenario: Renders variant sage
    When I render a Button with variant "sage"
    Then the button should have data-variant "sage"

  Scenario: Renders size xl
    When I render a Button with size "xl"
    Then the button should have data-size "xl"
