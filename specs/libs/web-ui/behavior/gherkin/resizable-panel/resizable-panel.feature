Feature: Resizable panel primitive

  As a developer using the web-ui design system
  I want a resizable panel primitive with a draggable, keyboard-accessible handle
  So that consuming apps can build resizable side rails that clamp to a safe width band

  Scenario: Widen the panel by dragging the handle right
    Given a resizable panel rendered at 250 pixels with a 150 to 350 pixel band
    When the user drags the separator handle 60 pixels to the right
    Then the panel width becomes 310 pixels

  Scenario: Dragging past the maximum stops at the maximum
    Given a resizable panel rendered at 340 pixels with a 150 to 350 pixel band
    When the user drags the separator handle 100 pixels to the right
    Then the panel width stops at 350 pixels

  Scenario: Widen the panel with the ArrowRight key
    Given the separator handle is focused on a panel at 250 pixels
    When the user presses ArrowRight
    Then the panel width increases by the keyboard step
    And the handle exposes the new width via aria-valuenow

  Scenario: The handle exposes separator semantics
    Given a resizable panel is rendered
    When the accessibility tree is inspected
    Then the handle has role "separator"
    And the handle has aria-orientation "vertical"

  Scenario: The handle's accessible label can be localized
    Given a resizable panel is rendered with a custom handle label "Ubah ukuran panel"
    When the accessibility tree is inspected
    Then the handle has aria-label "Ubah ukuran panel"
