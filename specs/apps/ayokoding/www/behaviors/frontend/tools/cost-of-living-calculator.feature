Feature: Salary savings calculator

  @unit @e2e
  Scenario: Cost-of-living breakdown lists category expenses per city
    Given I am on "/en/tools/cost-of-living-calculator"
    And the "Cost of living" tab is active
    When the page finishes loading
    Then I see a table of tech-hub cities
    And each row shows a Country column immediately to the left of the City column
    And each row shows monthly housing, food, transport, utilities, healthcare, childcare, school, and lifestyle expenses
    And each row shows an essentials subtotal and a total
    And each row shows a separate one-time relocation sunk-cost total
    And each row shows a separately labelled liquidity reserve

  @unit @e2e
  Scenario: Region narrows the country filter and country narrows the city filter
    Given I am on "/en/tools/cost-of-living-calculator"
    And the "Cost of living" tab is active
    When I select the region "ASEAN" then the country "Indonesia" in the cascading filters
    Then the Country filter lists only ASEAN countries
    And the City filter lists only Indonesian cities
    And only cities in Indonesia are shown in the table

  @unit @e2e
  Scenario: Country and city are always shown together on every tab
    Given I am on "/en/tools/cost-of-living-calculator"
    When I view any tab's results table
    Then every row shows a Country column immediately to the left of the City column

  @unit @e2e
  Scenario: Clicking a city name opens its single-city cost-of-living detail
    Given I am on "/en/tools/cost-of-living-calculator"
    When I click a city name in any table
    Then I am taken to that city's single-city Cost-of-living detail at "?city=<id>"
    And the City filter is pre-selected to that city
    And the detail shows the full per-category breakdown, essentials subtotal, total, healthcare scheme badge, and split relocation in both local currency and USD

  @unit @e2e
  Scenario: Clicking a country opens Cost-of-living filtered to that country
    Given I am on "/en/tools/cost-of-living-calculator"
    When I click a country name in any table
    Then I am taken to the Cost-of-living tab filtered to that country at "?country=<id>"
    And the Country filter is pre-selected to that country with its Region set
    And the table shows that country's cities as a filtered list rather than a single-city detail

  @unit @e2e
  Scenario: A city link takes precedence over a country link when both params are present
    Given I am on the calculator with both a country and a city query param set
    When the page resolves the deep link at "?tab=cost&country=<id>&city=<id>"
    Then the single-city Cost-of-living detail for the city is shown because a city implies its country

  @unit @e2e
  Scenario: Healthcare funding scheme is always shown
    Given I am on "/en/tools/cost-of-living-calculator"
    When I select any city on any tab
    Then a healthcare funding-scheme badge is shown for that city's country
    And the badge reads "tax-funded", "mandatory payroll insurance", or "out-of-pocket"

  @unit @e2e
  Scenario: The OOP abbreviation is explained on screen
    Given I am on a tab that shows the "Healthcare (OOP)" column
    When I read the legend near the table
    Then an on-screen explanation states that "OOP = out-of-pocket"
    And the explanation says it is the healthcare you pay yourself on top of any tax-funded or insurance coverage
    And every "OOP" acronym is wrapped in an abbr element titled "out-of-pocket"

  @unit @e2e
  Scenario: Relocation reserve is shown separately from sunk costs
    Given I am on the "Cost of living" tab
    When I read a city row
    Then the one-time relocation sunk-cost total is shown distinct from the monthly total
    And the liquidity-reserve cash cushion is shown in its own labelled figure, not folded into the sunk-cost total

  @unit @e2e
  Scenario: Savings tab converts gross salary to net before subtracting expenses
    Given I am on "/en/tools/cost-of-living-calculator"
    And I switch to the "Savings" tab
    When I enter a gross monthly salary of "8000" USD
    Then each city row shows a net take-home after the country's federal and sub-national effective tax
    And each row shows the essentials, the savings after essentials, and the savings after lifestyle with percentages
    And the table can be sorted by savings

  @unit
  Scenario: Savings tab honours the active geographic filter
    Given I am on "/en/tools/cost-of-living-calculator"
    And I switch to the "Savings" tab
    And I enter a gross monthly salary of "5000" USD
    When the Country filter is set to "Indonesia"
    Then the savings table lists only Indonesian cities
    And cities outside the selected scope are not shown

  @unit @e2e
  Scenario: Gross salary entered monthly shows the derived annual figure
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "8000" USD
    Then the annual gross is shown as "96000" USD
    And the annual figure equals twelve times the monthly figure

  @unit
  Scenario: Non-salary comp is shown as informational context only
    Given I am on the "Savings" tab with a gross salary entered
    When I read a city row
    Then a typical non-salary compensation (RSU/equity + bonus) figure is shown as a separate informational column
    But it is not added into the net, the essential savings, or the after-lifestyle savings

  @unit @e2e
  Scenario: Total compensation is shown for negotiation context
    Given I am on the "Savings" tab with a gross salary entered
    When I read a city row
    Then a total compensation figure equal to the base annual gross plus the typical non-salary comp is shown as informational context
    And the total compensation is not added into the net, the essential savings, or the after-lifestyle savings

  @unit @e2e
  Scenario: Sub-national tax lowers net only in federal countries
    Given I am on the "Savings" tab with a gross salary entered
    When I compare a US, Canadian, or Swiss city against a unitary-country city
    Then the federal-country city applies its city sub-national rate on top of the federal rate
    But the unitary-country city applies the federal rate alone

  @unit @e2e
  Scenario: Net take-home is lower than the entered gross
    Given I am on the "Savings" tab
    When I enter a gross monthly salary above a city's tax band threshold
    Then the net take-home shown for that city is lower than the entered gross

  @unit @e2e
  Scenario: Essentials above net show a deficit
    Given I am on the "Savings" tab for a high-cost city
    When I enter a gross salary whose net is lower than that city's modeled essentials
    Then the savings-after-essentials amount and percentage are shown as negative

  @unit @e2e
  Scenario: Indonesian locale is fully translated
    Given I am on "/id/tools/cost-of-living-calculator"
    When the page finishes loading
    Then all labels, category names, tax wording, healthcare-scheme labels, relocation labels, and the disclaimer are in Indonesian

  @unit @e2e
  Scenario: No Israeli cities are listed
    Given I am on the calculator in either locale
    When the page finishes loading
    Then no Israeli city appears in the dataset or any table

  @unit @e2e
  Scenario: Data snapshot date is clearly shown
    Given I am on the calculator
    When the page finishes loading
    Then I see a prominent "Data last updated" label with the dataset snapshot date
    And I see an "estimates only" disclaimer

  @unit @e2e
  Scenario: Every monetary figure converts to USD via the in-repo FX table
    Given I am on the calculator
    When I read any USD figure derived from a local-currency value
    Then the conversion uses the rate for that currency stored in the in-repo fx.ts table
    And every currency referenced by a city, country, role, or display-currency selector has an fx.ts entry

  @unit @e2e
  Scenario: Adding adults and children changes the modeled expenses
    Given I am on the "Cost of living" tab
    When I change the household from "single" to married with 2 school-age children
    Then the modeled housing and utilities increase sub-linearly
    And the modeled food and healthcare increase near per-capita
    And schooling is added for the two school-age children

  @unit @e2e
  Scenario: Pre-school children incur childcare, not schooling
    Given I am on the "Cost of living" tab
    When I set the household to 1 pre-school child and 0 school-age children
    Then the childcare expense is added for the one pre-school child
    But no schooling cost is added

  @unit
  Scenario: School type toggle is shown but disabled without school-age children
    Given I am on "/en/tools/cost-of-living-calculator"
    When the household has no school-age children
    Then the school-type toggle is shown but disabled
    And a hint explains that school-age children must be added to choose

  @unit @e2e
  Scenario: Private school raises expenses more than public
    Given I am on "/en/tools/cost-of-living-calculator"
    And the household has 2 school-age children
    When I switch the school type from "public" to "private"
    Then the schooling portion of the modeled expenses increases

  @unit @e2e
  Scenario: Rural area lowers housing versus city center
    Given I am on the "Cost of living" tab
    When I switch the area from "city center" to "rural"
    Then the modeled housing expense decreases
    And the city total decreases accordingly

  @unit
  Scenario: Minimum role for a savings target ranks on essential savings and is reordered
    Given I am on "/en/tools/cost-of-living-calculator"
    And I switch to the "Minimum role" tab
    And I set the baseline source to "savings target"
    When I enter a monthly savings target of "8000" USD
    Then I see the qualifying (city, role) rows grouped above a divider and non-qualifying rows dimmed below it
    And the lowest role rank that reaches at least 8000 USD essential savings anywhere in the filter is marked as the minimum
    And (city, role) rows that cannot reach 8000 USD essential savings are shown below the divider and de-emphasised

  # The reported "only one Malaysia entry / results hidden" bug. Each (city, role) is its own
  # candidate row — there is NO per-role argmax that keeps only one "best" city per role — so every
  # place that clears the bar within the filter is shown, a country can occupy several rows (one per
  # qualifying seniority level), and no qualifying country is hidden behind a higher-saving neighbour.
  @unit
  Scenario: Every qualifying city and role within the filter is included
    Given I am on the "Minimum role" tab with a baseline set
    And the geographic filter is the ASEAN region
    When the savings bar is cleared by several countries at several seniority levels
    Then every (city, role) whose essential savings is at or above the bar is shown as its own row
    And a country that clears the bar at more than one role appears on more than one row
    And no qualifying country is collapsed away behind another country's higher savings
    And rows are ordered by essential savings, highest first

  @unit @e2e
  Scenario: Roles are labelled as software-engineering roles
    Given I am on the "Minimum role" tab with a baseline set
    When the page finishes loading
    Then a caption states the ladder is software-engineering roles covering IC and management tracks

  @unit @e2e
  Scenario: Each role shows its per-country salary distribution
    Given I am on the "Minimum role" tab with a baseline set
    When I read a role row
    Then the role shows its country's p25, median, and p75 salary distribution
    And the row's essential savings is computed from the median salary

  @unit
  Scenario: A city row shows its country alongside the city name
    Given I am on the "Minimum role" tab with a baseline set
    When I read a qualifying (city, role) row
    Then the row shows the city and its country

  @unit
  Scenario: Geographic filter scopes the candidate cities
    Given I am on the "Minimum role" tab with a baseline set
    When I select the country "Indonesia" in the cascading filters
    Then every (city, role) row is drawn only from Indonesian cities

  @unit @e2e
  Scenario: Non-salary comp does not change the minimum-role ranking
    Given I am on the "Minimum role" tab with a baseline set
    When I compare two roles whose non-salary comp differs but whose median salary is equal
    Then their essential-savings ranking is unchanged because non-salary comp is informational only

  @unit @e2e
  Scenario: Lifestyle does not change the minimum-role ranking
    Given I am on the "Minimum role" tab with a baseline set
    When I change a city's lifestyle assumption
    Then the marked minimum role is unchanged because ranking is on essential savings only

  @unit @e2e
  Scenario: Minimum role from a reference city and role
    Given I am on the "Minimum role" tab
    And I set the baseline source to "Match a role"
    And I pick the city "Jakarta" and the role "Senior SWE"
    When I view the minimum role result
    Then the baseline savings bar equals that role's essential savings in Jakarta
    And the marked minimum role reaches at least that essential savings in absolute terms

  @unit
  Scenario: Minimum role from my own salary
    Given I am on the "Minimum role" tab
    And I set the baseline source to "my salary"
    When I enter my gross salary and its city
    Then the baseline savings bar equals my essential savings in my selected salary city
    And the bar is not raised to a cheaper city's optimum that I do not live in
    And the ladder marks the lowest role that meets or beats it

  @unit
  Scenario: My-salary baseline accepts the gross in local currency or USD
    Given I am on the "Minimum role" tab
    And I set the baseline source to "my salary"
    And I pick the salary city "Singapore"
    Then I can enter my gross monthly salary in either Singapore's local currency or USD
    And the local-currency option follows the selected salary city
    And choosing the local currency converts the entered amount to USD using the fx snapshot before ranking

  @unit @e2e
  Scenario: Savings shown in USD, local, and display currency
    Given I am on the "Minimum role" tab with a baseline set
    When I choose a display currency
    Then each role row shows its essential savings in USD, the city's local currency, and the display currency

  @unit
  Scenario: Every money column on the Minimum-role tab is dual currency
    Given I am on the "Minimum role" tab with a baseline set and a display currency chosen
    When I read a role row
    Then every money column (p25, median, p75, non-salary comp, total comp, and essential savings) shows the display currency on the first line and the city's local currency on the second line
    And no money column shows only a single currency

  @unit @e2e
  Scenario: Household composition changes the minimum qualifying role
    Given I am on the "Minimum role" tab and the "SWE I" role qualifies for the "single" household basis
    When I change the household to "married with 2 children" and the area to "center"
    Then "SWE I" no longer qualifies because childcare, schooling, and central housing raise its essentials above its net
    And a more senior role becomes the marked minimum

  @unit @e2e
  Scenario: No role can reach the bar
    Given I am on the "Minimum role" tab
    When I set a savings target higher than any role's essential savings in any city
    Then the tool states that no role clears the bar
    And no row is marked as the minimum

  @unit @e2e
  Scenario: Cost-basis controls affect role candidates
    Given I am on the "Minimum role" tab with a baseline set
    When I change the household type or area
    Then the role candidates' savings and the marked minimum role update accordingly

  @unit @e2e
  Scenario: Low-confidence cells are flagged on the minimum-role tab
    Given I am on the "Minimum role" tab with a baseline set
    When the table renders
    Then cells with lower data confidence display a visual flag indicator

  @unit @e2e
  Scenario: No Israeli city appears among role candidates
    Given I am on the "Minimum role" tab with a baseline set
    When the page finishes loading
    Then no Israeli city appears as a candidate city for any role

  @unit @e2e
  Scenario: Zero or empty salary shows deficit with suppressed percentage
    Given I am on the "Savings" tab
    When the gross monthly salary field is empty or zero
    Then each city row shows a negative essential-savings amount equal to the negation of that city's essential expenses in USD
    And each percentage cell shows an em dash because there is no net income to compute a percentage from

  @unit @e2e
  Scenario: Rural area and multi-adult household multiply the housing estimate sub-linearly
    Given I am on the "Cost of living" tab
    And I set the household to 2 adults with no children
    When I switch the area from "city center" to "rural"
    Then the housing estimate in the expense preview decreases to base times subLinear 2 adults times 0.75
    And the essentials total in the preview decreases accordingly

  @unit @e2e
  Scenario: Selecting a city from the City filter opens its detail view
    Given I am on the "Cost of living" tab
    When I select a city from the City dropdown filter
    Then the single-city cost-of-living detail for that city is shown
    And the detail is identical to the one shown when clicking the city name in the table

  @unit @e2e
  Scenario: Income exactly at the low-to-mid threshold uses the mid band
    Given I am on the "Savings" tab
    When I enter a gross monthly salary at exactly the low-to-mid band threshold for a city
    Then that city's net take-home uses the mid band effective tax rate

  @unit @e2e
  Scenario: Mobile city cards show the country name alongside the city
    Given I am viewing the "Cost of living" tab on a viewport narrower than 768 px
    When the mobile city cards render
    Then each card header shows both the city name and its country name

  @unit
  Scenario: Zero savings target marks the lowest role as the minimum
    Given I am on the "Minimum role" tab
    And I set the baseline source to "savings target"
    When I enter a monthly savings target of zero USD
    Then the qualifying divider is shown
    And the qualifying divider element is rendered in the role ladder
    And the minimum marker appears on the lowest-ranked role in the ladder
    And the qualifying (city, role) rows whose savings are at or above zero appear above the divider

  @unit @e2e
  Scenario: Expense preview updates in real time when household controls change
    Given I am on the cost-of-living calculator
    And the default household is 1 adult with no children in city center
    When I change the Adults control to 2
    Then the Housing preview amount increases to base times subLinear 2 adults
    And the Childcare and School preview amounts remain zero
    And the Total preview updates immediately without a page reload

  # Reconciled 2026-06-21: all 9 controls now serialized (region/country/city/tab/adults/
  # preschool/schoolkids/schooltype/area); selecting country alone encodes only "country=id",
  # not "tab=cost" (default tab is omitted per encodeState default-stripping).
  @unit @e2e
  Scenario: Selecting filters updates the URL with all active query parameters
    Given a user is on the cost-of-living calculator page
    When the user selects Country "Indonesia" and City "Jakarta"
    Then the URL updates to include query parameters reflecting those selections
    And copying the URL and opening it in a new tab restores the same filter state

  # Reconciled 2026-06-22: the min-role baseline source (savings target / match a role / my
  # salary) and its inputs, plus the savings gross, are now part of the URL (single source of
  # truth) so deep links restore the full tab state.
  @unit
  Scenario: Min-role baseline source and inputs are serialized in the URL
    Given I am on the "Minimum role" tab
    When I set the baseline source to "my salary"
    And I enter my gross salary and its city
    Then the URL query string includes the baseline source and the entered salary inputs

  @unit
  Scenario: Savings gross salary is serialized in the URL
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "5000" USD
    Then the URL query string includes the entered gross salary

  @unit @e2e
  Scenario: Page title includes tool name on load
    Given a user navigates to the cost-of-living calculator
    When the page finishes loading with default filter state
    Then the browser tab title includes the name of the tool

  # ── Accepted proposals: SG-001…006, USS-001…005, SG-D-001…004 (Phase 4 grill 2026-06-20) ──

  # SG-001 — Negative salary input is clamped to zero
  @unit @e2e
  Scenario: Negative salary input is clamped to zero
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "-1000"
    Then the annual gross displayed is "0 USD"
    And each city row shows the same deficit as for a zero salary entry

  # SG-002 — Decimal salary computes annual gross correctly
  @unit @e2e
  Scenario: Decimal monthly salary produces correct annual gross
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "8000.5"
    Then the annual gross is shown as "96,006 USD"
    And the annual figure equals twelve times the monthly figure

  # SG-003 — Very large salary does not produce NaN or Infinity
  @unit @e2e
  Scenario: Very large salary produces valid savings figures
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "99999999"
    Then no city row shows "NaN" or "Infinity" in any column
    And each city row shows a positive net take-home

  # SG-004 — Selecting only a country updates the URL
  # Reconciled 2026-06-21: default tab ("cost") is omitted from the URL; only "country=id" is
  # encoded. The assertion that "tab=cost" appears in the URL was stale.
  @unit @e2e
  Scenario: Selecting only a country updates the URL country parameter
    Given a user is on the cost-of-living calculator page
    When the user selects Country "Indonesia" without selecting a city
    Then the URL query string includes "country=id"
    And opening that URL in a new tab shows only Indonesian cities in the table
    And the Country filter is pre-selected to "Indonesia"

  # SG-005 — School type toggle is enabled when school-age children >= 1
  @unit
  Scenario: School type toggle becomes enabled when school-age children is set to one or more
    Given I am on "/en/tools/cost-of-living-calculator"
    And the household has no school-age children
    And the school-type toggle is shown but disabled
    When I set the household to 1 school-age child
    Then the school type toggle is enabled with "Public" and "Private" options
    And the default selection is "Public"

  # SG-006 — Housing scales sub-linearly (1.25x) for a 2-adult household
  @unit @e2e
  Scenario: Housing preview scales sub-linearly for 2-adult household
    Given I am on the cost-of-living calculator
    And the default household is 1 adult with no children in city center
    When I change the Adults control to 2
    Then the Housing preview amount is exactly 1.25 times the 1-adult amount
    And the Utilities preview amount is exactly 1.25 times the 1-adult amount
    And the Food preview amount is exactly 1.5 times the 1-adult amount
    And the Transport preview amount is unchanged from the 1-adult amount

  # USS-001 — Savings tab empty-state when no salary entered
  @unit @e2e
  Scenario: Savings tab shows empty-state guidance when no salary entered
    Given a user has opened the Cost of Living Calculator
    When they click the Savings tab
    And the gross monthly salary field contains no value or zero
    Then the savings comparison table is not shown
    And an instructional message is shown
    And no negative savings figures are visible

  @unit @e2e
  Scenario: Savings tab shows results after salary is entered
    Given a user is on the Savings tab with the empty-state message displayed
    When they enter a positive gross monthly salary value
    Then the instructional message disappears
    And the savings comparison table is shown with computed savings figures

  # USS-002 — Minimum Role tab empty-state when no target entered
  @unit @e2e
  Scenario: Minimum Role tab shows empty-state when no target amount entered
    Given a user has opened the Cost of Living Calculator
    When they click the Minimum Role tab
    And the Monthly savings target field contains no value or zero
    Then the role comparison table is not shown
    And an instructional message is shown
    And no role salary data is visible

  # USS-003 — Area toggle confirms data update
  @unit
  Scenario: Area toggle shows selected state and confirms data update
    Given a user is on the Cost of Living tab
    And "City center" is the currently active area selection
    When the user clicks "Rural"
    Then the "Rural" button displays as the active/selected state
    And a visible signal confirms the table data has been recalculated for rural estimates

  # USS-004 — Tab name and sub-label are visually/aria distinct
  @unit @e2e
  Scenario: Tab sub-labels are visually separated from tab names
    Given a user views the Cost of Living Calculator tab bar
    When any tab is in the inactive state
    Then the tab primary name and its descriptive sub-label are visually distinct
    And the two pieces of text do not run together without a visual separator
    And a screen reader announces them as separate text nodes

  # USS-005 — Tools index renders localized text
  @unit @e2e
  Scenario: Tools index page renders all text in the active locale
    Given a user navigates to /en/tools
    When the page renders
    Then the page heading and the calculator link display readable English labels
    And no raw i18n key strings are visible

  @unit @e2e
  Scenario: Tools index page renders in Indonesian on /id/tools
    Given a user navigates to /id/tools
    When the page renders
    Then the heading and link labels are in Indonesian
    And no raw i18n key strings are visible

  # SG-D-001 — Dual-currency display in cost-of-living and savings tables
  @unit @e2e
  Scenario: Cost-of-living table shows local currency and USD for each expense cell
    Given the user is on the Cost of living tab at desktop width
    When the table renders with at least one city row
    Then every monetary cell shows the local currency amount and the USD equivalent
    And no money cell shows a bare integer without a currency label

  @unit @e2e
  Scenario: Savings table shows local currency and USD for net and savings columns
    Given the user is on the Savings tab with a gross salary entered
    When the table renders
    Then the Net, Essentials, Essential-savings, and After-lifestyle-savings columns show both local and USD amounts

  # SG-D-002 — covered by existing "Mobile city cards show the country name alongside the city"

  # SG-D-003 — Page heading matches tool identity
  @unit @e2e
  Scenario Outline: H1 matches the tool's official name in each locale
    Given the user opens "/<locale>/tools/cost-of-living-calculator"
    When the page renders
    Then the H1 reads "<expected_h1>"
    And the browser title starts with "Cost of Living Calculator"

    Examples:
      | locale | expected_h1               |
      | en     | Cost of Living Calculator |
      | id     | Kalkulator Biaya Hidup    |

  # SG-D-004 — id locale uses Indonesian city/country names in all table views
  @unit @e2e
  Scenario: Id locale cost-of-living table uses Indonesian translations
    Given the user is on "/id/tools/cost-of-living-calculator" at desktop width
    When the cost-of-living table renders
    Then the Country column shows Indonesian country names where translations exist
    And the City column shows Indonesian city names where translations exist

  @unit
  Scenario: Id locale minimum-role table uses Indonesian city names
    Given the user is on "/id/tools/cost-of-living-calculator" at desktop width
    And the Minimum role tab is active
    When the ladder table renders
    Then the City column shows Indonesian city and country names where translations exist

  # prd.md acceptance criteria — design-system controls, locale URL redirect, mobile nav
  @unit @e2e
  Scenario: Gross-salary input uses the design-system Input primitive
    Given the user is on the "Savings" tab
    When the tab renders
    Then the gross-salary field renders with a visible border, design-token radius, and padding
    And it is paired with a Label primitive

  @unit @e2e
  Scenario: Baseline selector is a segmented control
    Given the user is on the "Minimum role" tab
    When the tab renders
    Then the baseline-source control renders as a styled segmented button group, not a plain select

  @unit @e2e
  Scenario: Tab labels are clean single phrases
    Given the user views the tab bar at any breakpoint
    When the tab bar renders
    Then each tab trigger's visible text is its label only, with the description not fused into it

  @unit @e2e
  Scenario: Each tab has a visible description associated with its trigger
    Given the user views the calculator tab bar
    When the tab bar renders
    Then each of the three tabs has a visibly rendered description element associated with its trigger via aria-describedby
    And no tab description text is duplicated elsewhere on screen

  @unit @e2e
  Scenario: Uppercase locale URL redirects to canonical lowercase
    Given the user requests "/EN/tools/cost-of-living-calculator"
    When the middleware processes the request
    Then the server redirects to "/en/tools/cost-of-living-calculator"

  @unit @e2e
  Scenario: Mobile nav drawer shows localized site navigation
    Given the user opens the mobile nav drawer at 375px on the "/id/" locale
    When the drawer renders
    Then it shows the site's top-level navigation links
    And every drawer label is localized

  # ── URL state Phase 4 scenarios (added 2026-06-21) ──────────────────────────

  # URL-001 — Out-of-range numeric param is reset to its default on load
  @unit @e2e
  Scenario: An out-of-range numeric param is reset to its default on load
    Given a deep link with query string "adults=4"
    When the page resolves the deep link
    Then the Adults control shows "1"
    And the URL is rewritten to have no "adults" param

  # URL-002 — Full country name is dropped (only ISO id is valid)
  @unit @e2e
  Scenario: A full-country-name param is dropped on load
    Given a deep link with query string "country=Indonesia"
    When the page resolves the deep link
    Then the Country filter returns to "All countries"
    And the URL is rewritten to have no "country" param

  # URL-003 — Selecting a city backfills country and region
  @unit @e2e
  Scenario: Selecting a city under no prior filter backfills country and region
    Given I am on the calculator with no query string
    When I select the city "Jakarta"
    Then the URL query string includes "city=jakarta"
    And the Country filter shows "Indonesia" and the Region filter shows "ASEAN"

  # URL-004 — Selecting a broader region clears incompatible narrower filters
  @unit @e2e
  Scenario: Selecting a broader region clears an incompatible country and city
    Given I am on the calculator with query string "city=singapore"
    When I select the region "Europe"
    Then the URL query string includes "region=europe"
    But the URL query string does not include "country" or "city"

  # URL-005 — Contradictory region+city deep link resolves with narrower filter winning
  @unit @e2e
  Scenario: A contradictory region-and-city deep link resolves with the narrower filter winning
    Given a deep link with query string "region=europe&city=singapore"
    When the page resolves the deep link
    Then the single-city detail for Singapore is shown
    And the URL is rewritten to canonical form with "city=singapore" and "region" backfilled to "asean"

  # URL-006 — City-detail back link preserves an explicitly chosen parent geo scope.
  # When the user explicitly selected region+country before opening a city, the back
  # link returns to that scope. (A city-ONLY deep link, where scope was auto-derived,
  # instead returns to the bare calculator — see the UWT-015 scenario below.)
  @unit @e2e
  Scenario: The city-detail back link preserves the parent geo scope
    Given I am on the single-city detail with query string "region=asean&country=sg&city=singapore"
    When I activate the "Back to all cities" link
    Then the URL query string includes "region=asean" and "country=sg"
    But the URL query string does not include "city"

  # URL-007 — Tab change is written to the URL
  @unit @e2e
  Scenario: Changing the tab writes the tab to the URL
    Given I am on the calculator with no query string
    When I switch to the "Savings" tab
    Then the URL query string includes "tab=savings"
    And reloading the page keeps the "Savings" tab active

  # URL-008 — Cost-basis control change is written to the URL
  @unit @e2e
  Scenario: Changing a cost-basis control writes it to the URL
    Given I am on the calculator with no query string
    When I change the Adults control to "2"
    Then the URL query string includes "adults=2"
    And the household preview updates without a page reload

  # URL-009 — Breadcrumb offers Home and Tools escape links
  @unit @e2e
  Scenario: The breadcrumb offers an escape to the Tools index and Home
    Given I am on the calculator with query string "city=singapore"
    When I read the breadcrumb above the page title
    Then a "Home" link to "/en" is shown
    And a "Tools" link to "/en/tools" is shown

  # AC-2 (DWT-B-003/DWT-B-004) — Breadcrumb uses the shared primitive with chevron separators
  @unit @e2e
  Scenario: The breadcrumb separates crumbs with chevrons, not a literal slash
    Given I am on the calculator with query string "city=singapore"
    When I read the breadcrumb above the page title
    Then the crumbs are separated by chevron icons
    And no literal "/" separator is shown between crumbs

  # AC-3 (UWT-013) — Final breadcrumb crumb equals the page H1 in each locale
  @unit @e2e
  Scenario Outline: The final breadcrumb crumb matches the page title in each locale
    Given the user opens "/<locale>/tools/cost-of-living-calculator"
    When the breadcrumb renders
    Then the current-page crumb text reads "<expected_title>"
    And the current-page crumb is marked aria-current="page"

    Examples:
      | locale | expected_title            |
      | en     | Cost of Living Calculator |
      | id     | Kalkulator Biaya Hidup    |

  # URL-010 — Region selection writes region to the URL
  @unit @e2e
  Scenario: Selecting a region writes the region to the URL
    Given I am on the calculator with no query string
    When I select the region "Europe"
    Then the URL query string includes "region=europe"
    And the URL query string does not include "country" or "city"

  # URL-011 — City deep link restores city and backfills country and region
  @unit @e2e
  Scenario: A city deep link restores the city and backfills country and region
    Given a deep link with query string "city=singapore"
    When I open that link in a fresh tab
    Then the single-city Cost-of-living detail for Singapore is shown
    And the Country filter shows "Singapore" and the Region filter shows "ASEAN"

  # URL-012 — Unknown city param is dropped on load
  @unit @e2e
  Scenario: An unknown city param is dropped on load
    Given a deep link with query string "city=atlantis"
    When the page resolves the deep link
    Then the City filter returns to "All cities"
    And the URL is rewritten to have no "city" param

  # URL-013 — Canonicalization uses replace so Back button skips the dirty URL
  @unit @e2e
  Scenario: Canonicalization does not add a browser history entry
    Given a deep link with query string "city=atlantis"
    When the page rewrites the URL to canonical form
    Then pressing the browser Back button does not return to the "city=atlantis" URL

  # AC-4 (UWT-016/DWT-005) — Geo-filter selects meet the 44px minimum touch target
  @unit @e2e
  Scenario: Geo-filter selects meet the minimum touch-target height on mobile
    Given I am on the calculator at a 375px-wide viewport
    When the geo-filter selects render
    Then each geo-filter select is at least 44 pixels tall

  # AC-5 (UWT-008) — Calculator page does not overflow horizontally at 320px
  @unit @e2e
  Scenario: The calculator page has no horizontal overflow at 320px
    Given I am on the calculator at a 320px-wide viewport
    When the calculator page renders
    Then the document does not scroll horizontally

  # EWT-R01 (regression of UWT-008) — the longer Indonesian tab labels must not
  # widen the document beyond 320px either.
  @unit @e2e
  Scenario: The calculator page has no horizontal overflow at 320px in the id locale
    Given I am on the id-locale calculator at a 320px-wide viewport
    When the calculator page renders
    Then the document does not scroll horizontally

  # AC-8 (UWT-004) — Savings gross-salary field surfaces the active currency, not a hardcoded label
  @unit @e2e
  Scenario: The Savings gross-salary field shows the active currency as a separate indicator
    Given I am on the "Savings" tab
    When the gross-salary field renders
    Then the gross-salary label does not contain the literal currency code "USD"
    And an active-currency indicator next to the field shows "USD"

  # UWT-019 — the fixed USD indicator is accompanied by a short explanation of why USD
  # is used for every city, so it is not mistaken for a missing currency selector.
  @unit @e2e
  Scenario: The Savings currency indicator explains why USD is used for every city
    Given I am on the "Savings" tab
    When the gross-salary field renders
    Then an explanation states salaries are compared in USD across all cities

  # AC-9 (UWT-006) — Minimum-role tab shows empty-state guidance for a BLANK savings target only
  @unit @e2e
  Scenario: A blank savings target shows empty-state guidance instead of the role ladder
    Given I am on the "Minimum role" tab with the savings-target baseline and a blank target
    When the tab renders
    Then a minimum-role empty-state guidance message is shown
    But entering an explicit zero target replaces the guidance with the role ladder and its divider

  # AC-10 (UWT-007) — Region selector lists exactly the nine intended regions
  @unit @e2e
  Scenario: The region selector lists exactly the nine intended regions
    Given I am on the calculator with no query string
    When the region filter renders
    Then the region selector offers exactly the nine regions africa, americas, asean, asia, europe, japan, mena, nordics, and oceania

  # AC-11 (UWT-014) — A country change that auto-changes the region surfaces an advisory
  @unit @e2e
  Scenario: Selecting a country that changes the region shows a visible advisory
    Given I am on the calculator with no region selected
    When I select a country whose region differs from the current selection
    Then a visible region-auto-advisory message is shown

  # AC-12 (UWT-015) — A city-only deep link returns to the bare calculator
  @unit @e2e
  Scenario: A city-only deep link back link omits the auto-derived region and country
    Given a deep link with query string "city=london"
    When I read the single-city detail back link
    Then the back link points to the bare calculator "?tab=cost" with no region or country

  # ── Phase 7: spec coverage sweep ──────────────────────────────────────────────

  # SG-U-001..004 (URL default-stripping): switching back to the default tab removes
  # the tab param so the URL stays clean.
  # Scenario: Switching to a non-default tab then back to the default tab removes the tab param
  #   Given I am on the calculator with no query string
  #   When I switch to the "Savings" tab and then switch back to the "Cost of living" tab
  #   Then the URL query string does not include a "tab" parameter

  # SG-U (country-narrows-city) — selecting a country without a region narrows the city dropdown
  @unit @e2e
  Scenario: Selecting a country without a region still narrows the city dropdown
    Given I am on the calculator with no region or country selected
    When I select the country "Indonesia" in the country filter without first selecting a region
    Then the city dropdown lists only cities in Indonesia

  # SG-U (area radiogroup) — the area control renders with role="radiogroup"
  @unit @e2e
  Scenario: The area control is rendered as a radiogroup
    Given I am on the cost-of-living calculator
    When the cost-basis controls render
    Then the area segmented control has role="radiogroup"
    And the area radiogroup contains the "City center" and "Rural" options

  # SG-U (baseline SegmentedControl) — baseline selector is a radiogroup that shows or
  # hides the relevant sub-form depending on which option is active
  @unit @e2e
  Scenario: The baseline selector shows the savings-target sub-form when savings target is selected
    Given the user is on the "Minimum role" tab
    When the tab renders
    Then the baseline-source control renders as a radiogroup with at least three options
    And the savings-target input is visible when savings target is the selected baseline
    And the reference-role inputs are hidden when savings target is the selected baseline

  # Regression — changing a filter must not scroll the page back to the top. The URL write is
  # in-page view state, not a page navigation, so it requests { scroll: false }.
  @unit
  Scenario: Changing a filter preserves the scroll position
    Given I am on the cost-of-living calculator
    When I change the region filter to "Europe"
    Then the URL update requests no scroll so the page does not jump to the top

  # Regression — typing a salary must not write the URL on every keystroke (the stutter bug).
  # The field echoes each keystroke instantly while the URL commit is debounced until typing
  # settles.
  @unit
  Scenario: Typing the gross salary echoes instantly but commits to the URL only after typing settles
    Given I am on the "Savings" tab
    When I type a gross monthly salary of "7000" without pausing
    Then the salary field immediately shows "7000"
    And the gross salary is written to the URL once typing settles

  # Public primary schooling is not open to foreign residents in every country. Where it is not
  # fully open (limited or nationals-only — e.g. Singapore, Indonesia, UAE), a relocating foreigner
  # cannot realistically use it, so the calculator charges the PRIVATE figure and flags the cell.
  @unit
  Scenario: Public schooling not open to foreigners is charged at the private rate
    Given I am on the cost-of-living calculator
    When I add one school-age child with public school selected
    Then the Singapore school cost equals its private-school figure and the cell is flagged

  # Where public schooling IS open to foreign residents (e.g. Germany), the public figure stands.
  @unit
  Scenario: Public schooling open to foreigners keeps the public cost
    Given I am on the cost-of-living calculator
    When I add one school-age child with public school selected
    Then the Berlin school cost equals its public-school figure with no foreigner flag

  # ── Phase 8: UX-hardening fold-in (SG-001..003, USS-001..004, protected behaviours) ──
  # Accepted spec proposals from the 2026-06-22 three-lens retest (see plan
  # ayokoding-www-calculator-ux-hardening). Each scenario protects a behaviour that
  # landed in Phases 1-7 so feature-change-completeness holds.

  # Cluster 1 / SG-001 — only the active tab description is visible; it follows the tab.
  @unit
  Scenario: Only the active tab description is visible
    Given the cost-of-living calculator is open with the "Cost of living" tab active
    When the page is rendered
    Then the "Cost of living" tab description is visible
    And the "Savings" tab description is not visible
    And the "Minimum role" tab description is not visible

  @unit
  Scenario: Active tab description follows the active tab
    Given the cost-of-living calculator is open with the "Cost of living" tab active
    When the user selects the "Savings" tab
    Then only the "Savings" tab description is visible

  # Cluster 2 — touch targets + segmented/sort a11y.
  @unit
  Scenario: Interactive controls meet the 44px touch target
    Given the calculator at 375px
    When the page is rendered
    Then every tab trigger is at least 44px tall
    And every school-type, area, and salary-currency segmented radio is at least 44px tall

  # USS-003 — Area toggle exposes its active state via ARIA.
  @unit
  Scenario: Area toggle exposes its pressed state
    Given "City center" is the active area
    When the page is rendered
    Then the "City center" button has aria-pressed "true"
    And the "Rural" button has aria-pressed "false"

  # USS-004 — disabled school-type buttons announce the prerequisite.
  @unit
  Scenario: Disabled school-type buttons announce the prerequisite
    Given "School-age children" is 0
    When the page is rendered
    Then the "Public" and "Private" buttons are aria-disabled
    And their accessible description names the "add school-age children" prerequisite

  @unit
  Scenario: Sortable savings column exposes aria-sort
    Given the Savings tab table is shown
    When the page is rendered
    Then the sortable "Savings after essentials" column header has an aria-sort value

  # Cluster 3 — foreigner public-school flag clear, styled, and present in both views.
  @unit
  Scenario: Foreigner-school flag is clear, styled, and present in both views
    Given a city whose country does not open public school to foreigners
    And school-age children >= 1 and school type "public"
    When the page is rendered
    Then the cost-of-living table school cell shows a clearly-worded private-fallback flag
    And the flag is visually distinct from ordinary caption text
    And the city-detail school row renders the school-foreigner-flag-<cityId> testid

  # Cluster 4 — jargon glosses, localized OOP abbr title, localized region names.
  @unit
  Scenario: Jargon table headers carry an accessible explanation
    Given the calculator is open
    When the page is rendered
    Then the "Healthcare (OOP)" header has a title explaining out-of-pocket (localized)
    And the "Relocation (sunk)" and "Liquidity reserve" headers carry explanatory titles
    And the "P25"/"Median"/"P75" headers carry percentile explanations
    And the "Track" column abbreviations ic/mgmt are expanded or carry abbr titles

  # Protected behaviour — the OOP abbr title is localized (id != literal "out-of-pocket").
  @unit
  Scenario: The OOP abbreviation title is localized per locale
    Given the calculator is open
    When the page is rendered
    Then the localized out-of-pocket title differs between the en and id locales
    And the id-locale out-of-pocket title is not the literal English "out-of-pocket"

  # Protected behaviour — region option display names are localized while the serialized
  # region key stays English for URL stability.
  @unit
  Scenario: Region option display names are localized but the serialized key stays English
    Given the calculator is open
    When the region filter renders
    Then each region option's serialized value is its English key
    And the region display label differs between the en and id locales

  @unit
  Scenario: Healthcare scheme badges use consistent casing
    Given the calculator is open
    When the page is rendered
    Then no healthcare-scheme badge is rendered in ALL CAPS while another is lower-case

  # Cluster 5 / USS-001 + USS-002 — UX states.
  @unit
  Scenario: Savings tab guides the user to enter a salary
    Given the Savings tab is activated with no salary entered
    When the tab activation occurs
    Then a prominent empty-state prompt is shown in the data area
    And the gross salary input receives focus

  @unit
  Scenario: Minimum-role tab does not render the single-city essentials preview
    Given the Minimum-role tab is activated
    When the page is rendered
    Then no "Example — estimated monthly essentials" single-city cost preview is shown
    # The min-role tab now lists every qualifying city, so a one-city example is redundant there.

  @unit
  Scenario: Savings salary input shows its currency at the field
    Given the Savings tab is shown
    When the page is rendered
    Then the gross salary input displays its USD currency inline at the field

  # Cluster 6 / SG-002 + SG-003 — design-system fidelity.
  @unit
  Scenario: All selects share the design-system chrome
    Given the calculator at 1280px
    When the page is rendered
    Then every <select> has computed appearance "none" and a custom chevron affordance
    And no <select> shows the browser's native dropdown arrow

  @unit
  Scenario: Baseline-source control keeps the 44px rhythm at mobile
    Given the Minimum-role tab at 320px and 375px
    When the page is rendered
    Then the "Baseline source" segmented control height does not exceed 44px

  @unit
  Scenario: Salary-currency toggle bottom-aligns with its sibling input
    Given the Minimum-role "My salary" baseline at 1280px
    When the page is rendered
    Then the salary-currency toggle bottom-aligns with the gross salary input
