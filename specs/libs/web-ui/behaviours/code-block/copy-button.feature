Feature: CopyButton primitive

  A standalone, reusable copy affordance that writes a value to the clipboard, confirms success via
  an icon swap and a polite live region, reverts after a timeout, and stays fully keyboard- and
  screen-reader-operable.

  Scenario: Clicking the copy button writes its value to the clipboard
    Given a CopyButton rendered with the value "npm install"
    When the user clicks the button
    Then the clipboard receives the exact text "npm install"

  Scenario: A successful copy swaps to the success icon and announces via a live region
    Given a CopyButton rendered with a value and a stubbed clipboard that resolves
    When the user clicks the button
    Then the button shows the success (Check) icon
    And a polite live region announces the copied label

  Scenario: The success state reverts to the resting state after the timeout
    Given a CopyButton that has just shown its success state
    When the revert timeout elapses
    Then the button shows the resting (Copy) icon again
    And the live region no longer announces the copied label

  Scenario: A failed clipboard write does not show a false success state
    Given a CopyButton rendered with a stubbed clipboard that rejects
    When the user clicks the button
    Then the button does not show the success (Check) icon
    And no copied confirmation is announced

  Scenario: The copy button is operable by keyboard
    Given a CopyButton is focused
    When the user presses Enter
    Then the clipboard receives the button's value

  Scenario: The copy button exposes an accessible name
    Given a CopyButton rendered with the default labels
    When the accessibility tree is inspected
    Then the button has an accessible name of "Copy"

  Scenario: The copy button's accessible name can be localized
    Given a CopyButton rendered with copyLabel "Salin"
    When the accessibility tree is inspected
    Then the button has an accessible name of "Salin"

  Scenario: The copy button has no accessibility violations
    Given a CopyButton is rendered in its resting state
    When an automated accessibility scan runs
    Then no accessibility violations are reported

  Scenario: The copy button meets the minimum target size
    Given a CopyButton rendered at its default size
    When its rendered box is measured
    Then both dimensions are at least 24 CSS pixels

  Scenario: Re-clicking during the success window resets the revert timer
    Given a CopyButton has just shown its success state from a first click
    When the user clicks the button again before the revert timeout elapses
    Then the button remains in the success (Check) state
    And the revert timeout is measured from the second click, not the first

  Scenario: A retry after a failed clipboard write succeeds normally
    Given a CopyButton whose previous click failed to write to the clipboard
    When the user clicks the button again and the clipboard write resolves
    Then the button shows the success (Check) icon
    And a polite live region announces the copied label

  Scenario: The copy button is operable by keyboard via the Space key
    Given a CopyButton is focused
    When the user presses Space
    Then the clipboard receives the button's value

  Scenario: A failed clipboard write shows an error cue and announces it
    Given a CopyButton rendered with a stubbed clipboard that rejects
    When the user clicks the button
    Then the button shows the error (X) icon
    And a polite live region announces the error label

  Scenario: The copy button exposes a native tooltip title
    Given a CopyButton rendered with the default labels
    When the button's attributes are inspected
    Then the button carries a title matching its accessible name
