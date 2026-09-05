Feature: Resizable Docs Sidebar

  As a reader visiting AyoKoding docs
  I want to resize the desktop navigation rail and have its width persist
  So that I can tune the sidebar to my screen and content without losing that choice

  Background:
    Given the app is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Persist the chosen width across a reload
  @integration-exempt
  Scenario: Persist the chosen width across a reload
    Given the reader has resized the docs sidebar to 320 pixels on a desktop viewport
    When the reader reloads the page
    Then the docs sidebar renders at 320 pixels

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Hide the resizable rail below the md breakpoint
  @integration-exempt
  Scenario: Hide the resizable rail below the md breakpoint
    Given the docs page is open at a 375 pixel viewport
    When the layout renders
    Then the resizable aside is not displayed
    And navigation is available through the mobile drawer

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Scroll the sidebar horizontally when a label overflows
  @integration-exempt
  Scenario: Scroll the sidebar horizontally when a label overflows
    Given a docs sidebar narrowed to 150 pixels containing a nav label wider than 150 pixels
    When the reader views the sidebar
    Then the sidebar content area is horizontally scrollable
    And the label is not clipped or wrapped

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Overflowing nav labels signal that more content is scrollable
  @integration-exempt
  Scenario: Overflowing nav labels signal that more content is scrollable
    Given the docs sidebar is narrowed enough that a nav label's text exceeds the visible rail width
    When the reader views the sidebar without scrolling it
    Then a visible cue indicates the label continues off-screen
    And the item's expand-or-collapse chevron remains visible

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Scroll the sidebar vertically when the nav tree is taller than the viewport
  @integration-exempt
  Scenario: Scroll the sidebar vertically when the nav tree is taller than the viewport
    Given a docs sidebar whose nav tree is taller than the visible rail height
    When the reader views the sidebar
    Then the sidebar content area is vertically scrollable
    And the horizontal scroll behaviour is unaffected

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Apply a preset width to the mobile nav drawer
  @integration-exempt
  Scenario: Apply a preset width to the mobile nav drawer
    Given the mobile nav drawer is open at a 375 pixel viewport
    When the reader selects the wider preset
    Then the drawer renders at the wider preset width

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The resize handle's accessible label is localized
  @integration-exempt
  Scenario: The resize handle's accessible label is localized
    Given the docs page is open in the "id" locale
    When the layout renders
    Then the resize handle's aria-label is the "id" translation of "Resize panel"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / An invalid persisted preset width falls back to the mobile drawer's default
  @integration-exempt
  Scenario: An invalid persisted preset width falls back to the mobile drawer's default
    Given the mobile nav drawer has a corrupted persisted preset width
    When the mobile nav drawer opens at a 375 pixel viewport
    Then the drawer renders at the default preset width

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The drawer's width-preset control shows a visible caption
  @integration-exempt
  Scenario: The drawer's width-preset control shows a visible caption
    Given the mobile nav drawer is open at a 375 pixel viewport
    When the reader looks at the width-preset buttons
    Then a visible caption explains that the buttons control the drawer's width
