# Product Requirements Document — Cost of Living Calculator

## Product Overview

The **Cost of Living Calculator** is an interactive, client-side tool on `ayokoding-www` that models
the real cost of living and savings across tech-hub cities worldwide. It lives at
`/[locale]/tools/cost-of-living-calculator`, works in both English (`en`) and Indonesian (`id`), and
is organised into **three distinct tabs**. (The tool spans cost-of-living + savings + minimum-role,
but its user-facing name and route are **cost-of-living-calculator**; the plan folder keeps its
original `ayokoding-www-salary-savings-calculator` slug.)

Its two intended uses are **real salary negotiation** (read a role's p25/median/p75 distribution +
typical non-salary comp → total compensation to benchmark an offer and set a target) and
**relocation evaluation** (read net-of-tax take-home, full expense composition, two savings figures,
and one-time relocation budget per city). Both are reachable from the three tabs below — no extra
tab is introduced.

All three tabs share a **Region → Country → City** cascading filter group (region narrows countries;
country narrows cities), and every row **always shows both Country and City** (a Country column
immediately to the left of the City column) where **both the Country name and the City name are links**.
Clicking either navigates to the **Cost-of-living tab with the related geographic filter pre-selected**:
clicking a **City name** opens that city's single-city **Cost-of-living detail** view (deep-linkable as
`?tab=cost&city=<id>`); clicking a **Country name** opens the **Cost-of-living tab filtered to that
country** — that country's cities as a filtered list, not a single-city detail (deep-linkable as
`?tab=cost&country=<id>`). A city click takes precedence if both params are present (a city implies its
country).

1. **Cost of living** — _"How much do I need to live in each hub?"_ No salary input. Per city, the
   full monthly **expense-category breakdown** (housing, food, transport, utilities, healthcare,
   childcare, school, lifestyle) with an essentials subtotal and a total, plus a separate one-time
   **relocation sunk-cost** line and a separately labelled **liquidity reserve**. Lists tech-hub
   cities worldwide, filtered via the shared Region / Country / City filters; each **city name links to
   its single-city detail** and each **country name links to the Cost-of-living tab filtered to that
   country**.
2. **Savings** — _"For my gross salary, where do I save most across cities?"_ Enter a **gross salary**
   (USD) **monthly or annual** (enter one, both are shown; annual = 12 × monthly). For each city the
   tool converts gross to **net take-home** via the country's federal banded effective tax rate plus
   any city sub-national rate, subtracts the modeled essentials, and shows **both savings figures**
   (savings after essentials, savings after lifestyle) with percentages across cities, sortable; a
   separate informational **non-salary comp** (RSU/equity + bonus) column gives total-comp context.
3. **Minimum role** — _"For a savings baseline, what is the lowest **software-engineering** role
   (anywhere) that clears it?"_ Set a savings **baseline** (own salary, a reference city + role, or a
   raw savings target), and the tool runs every role's **median** salary through the same **net →
   essentials → essential savings** engine, ranks roles by absolute USD **essential savings**
   (lifestyle excluded), marks the **lowest qualifier**, and **reorders** the ladder so qualifying
   roles sit above the minimum and non-qualifying roles sit below a divider. The ladder is explicitly
   a **software-engineering (IC + management)** ladder.

All figures come from static, curated, `web-researcher`-sourced datasets. Every modeled value is
**confidence-tiered** (`high` | `moderate` | `proxy`) and **snapshot-dated**. The tool is fully
client-side rendered — no backend, no runtime network.

## Personas

- **Tech worker / visitor** — has a salary in mind, wants to see where and how much they could save
  net of tax and real living costs.
- **Relocation planner** — compares many cities at once, needs both the monthly expense breakdown
  and the one-time relocation budget to shortlist destinations.
- **Career planner / job seeker** — has a savings goal, wants to know the lowest engineering role
  (and where) that meets it.
- **Indonesian visitor** — uses the `id` locale; expects fully localized labels and number/currency
  formatting.

## Geographic filters (shared, all tabs)

All three tabs share a **Region → Country → City** cascading filter group. Selecting a **Region**
narrows the **Country** list; selecting a **Country** narrows the **City** list; each level is
clearable (clearing a higher level resets the lower ones). On the Cost-of-living and Savings tabs the
filters narrow the visible rows; on the Minimum-role tab they **scope the candidate cities** (each
role's best city is chosen within the filtered set). The old single-country-only filter is replaced by
this cascading group; the removed "single-city breakdown" mode is now the **city-detail drill-down**
(below).

Every table row **always shows both Country and City** — a **Country column immediately to the left of
the City column** (on mobile cards the heading reads "City, Country") — and **both the Country name and
the City name are links** on every tab. Each navigates to the **Cost-of-living tab with the related
geographic filter pre-selected**:

- **Clicking any city name anywhere** (on any tab) navigates to the single-city **Cost-of-living
  detail** view: the Cost-of-living tab scoped to that one city (its City filter pre-selected), showing
  the full per-category breakdown, essentials subtotal, total, healthcare scheme badge, and the split
  relocation (sunk + liquidity reserve), all dual-currency. It is **deep-linkable** via
  `?tab=cost&city=<id>` and offers a back affordance to the full table.
- **Clicking any country name anywhere** (on any tab) navigates to the **Cost-of-living tab filtered to
  that country** — the Country filter (and its Region) pre-selected so the table shows that country's
  cities as a filtered list (NOT a single-city detail). It is **deep-linkable** via
  `?tab=cost&country=<id>`.

Both integrate with the existing Region → Country → City cascading filter: a country click sets the
Country filter (and its Region); a city click sets the City filter (and its Country + Region). A city
click takes **precedence** if both `country` and `city` query params are present, because a city
implies its country.

## Tabs

The page has three tabs selected by a tab toggle.

- **Cost of living** — no salary input. A table of tech-hub cities, a **Country column to the left of
  the City column**, each row showing the seven monthly expense categories (housing, food, transport,
  utilities, healthcare, **childcare**, lifestyle) plus the **school** add-on, an **essentials
  subtotal** (housing + food + transport + utilities + healthcare + childcare + school), a **total**
  (essentials + lifestyle), a separate one-time **relocation sunk-cost** total, and a **separately
  labelled liquidity reserve** (the cash cushion the user keeps). Each **city name links to its
  single-city detail** and each **country name links to the Cost-of-living tab filtered to that
  country**. Each tab also **always shows the healthcare funding scheme** for the selected
  city/country (a badge: "Healthcare: tax-funded (NHS-style)" / "mandatory payroll insurance" /
  "out-of-pocket"), plus a **"health insurance: compulsory / optional"** indicator. The **Healthcare
  (OOP)** column header is explained on screen — **OOP = out-of-pocket**, the healthcare you pay
  yourself on top of any tax-funded or insurance coverage — via a legend/footnote line on every tab that
  shows the column. The shared Region / Country / City filters narrow the table.
- **Savings** — one **gross salary** input accepted as **monthly or annual** (enter one, the tool
  shows both; annual = 12 × monthly), in USD. For each city the tool computes
  **net = gross × (1 − (federalRate[band] + subNationalRate[band]))** via the country's federal banded
  tax model plus any city sub-national rate (US states / Canada provinces / Switzerland cantons), then
  derives **two savings figures** — `essentialSavings = net − essentials` and
  `afterLifestyleSavings = essentialSavings − lifestyle` — and shows **both amounts + both
  percentages** (each in local + USD), sortable. Columns include the Country+City (**both the Country
  and the City name are links** — City → that city's detail, Country → the Cost-of-living tab filtered
  to that country), the gross monthly
  AND annual, a typical **non-salary comp** (RSU/equity + bonus, informational total-comp context only
  — NOT in the savings math), a derived **total compensation** figure (base annual + non-salary comp,
  informational, for negotiation context), the income band + effective tax %, net, essentials, and the
  two savings figures.
- **Minimum role** — a savings **baseline** plus a ranked **software-engineering** role ladder
  (IC + management tracks; a caption states this). The baseline is set one of three ways: (a) **my
  salary** — enter a gross salary (and its city/country) and the tool computes its essential savings;
  (b) **reference role** — pick a city + role and use that role's computed essential savings there
  (using the role's **median** salary); (c) **savings target** — type a raw monthly savings amount in
  a chosen currency. The tool normalises the baseline to USD and ranks every role on the ladder by its
  best (cheapest-qualifying) city's absolute **essential savings** (using each role × country's
  **median** salary; lifestyle EXCLUDED — it is a personal-preference variable), marking the **lowest
  role** that clears the bar. The ladder is **reordered**: qualifying roles are grouped high→low down
  to the marked MINIMUM, then a divider, then the dimmed **non-qualifying ("below minimum")** roles.
  Each row shows the best city **and its country** (**both the best-city name and the country name are
  links** — best-city → that city's Cost-of-living detail, country → the Cost-of-living tab filtered to
  that country), the role × country **p25 / median / p75** salary
  distribution, a typical **non-salary comp**, a derived **total compensation** (base + non-salary
  comp, informational, for negotiation context), and the **essential savings**. **Every money column on
  this tab — p25, median, p75, non-salary comp, total comp, and essential savings — is shown dual
  (display currency on line 1 + the best city's local currency on line 2)**, consistent with the
  universal "local + USD everywhere" rule; the display-currency selector simply chooses which currency
  fills line 1 (defaulting to USD). The Region / Country / City filters scope the candidate cities, and
  the **shared household / area / school-type cost-basis controls** (the same set shown on the other two
  tabs) apply here too — the minimum qualifying role depends on the household and area, because a role's
  essential savings falls as the modeled essentials rise. For example, **SWE I may be enough if you are
  single, but not if you have two children and live in the city center**, where childcare, schooling,
  and central housing push essentials above the role's net.

The **household**, **area**, and **school-type** cost-basis controls below — together with the
**Region / Country / City** geographic filters — form a **single shared control set that applies on all
three tabs, including Minimum role** (they shape the modeled expenses used in every figure, including the
role candidates'; the Minimum-role essential-savings computation uses the active household / area /
school basis). Across all three tabs **every monetary figure — including each salary percentile (p25 /
median / p75), each compensation figure (non-salary comp, total comp), each expense category, and each
savings figure — is shown in both the city's local currency and USD**; the minimum-role tab adds a
**display-currency** selector so figures can additionally be read in a user-chosen currency (the
selector chooses which currency occupies the primary line alongside the local figure).

A **household control** applies to all three tabs and sets the cost-of-living basis. The household is
specified as:

- **single** vs **married** (1 or 2 adults), and
- a count of **pre-school-age children** (0–3) and a count of **school-age children** (0–3), entered
  as two small number inputs.

The household scales the modeled expenses on an **OECD-modified equivalence basis** (first adult 1.0,
+0.5 per extra adult, +0.3 per child): **housing + utilities** scale **sub-linearly** (economies of
scale) while **food, healthcare, and childcare** scale **near per-capita**. **Pre-school-age children
incur childcare**; **school-age children incur schooling**. When the household has school-age
children, a **school-type toggle** (`public` | `private`) applies. Each city carries a **median**
monthly childcare cost per pre-school child and a **median** monthly school cost per school-age child
for both school types; childcare and schooling are added on top of the modeled categories, multiplied
by the respective child counts. The school-type toggle is hidden when there are no school-age children.

An **area toggle** (`center` | `rural`) sets where in the city the person lives. The city-center
baseline is the dataset's stored cost; the rural option applies a discount (mainly to **housing**)
via a shared area-multiplier. The area toggle applies to the modeled categories only, not childcare
or schooling.

## UI Design — Cost-of-Living Screen (Design Funnel)

The stakeholder has **selected Option A — Category Table** from the low-fidelity alternatives. The
low-fi ASCII alternatives (≥2) and a mobile/tablet/desktop responsive strategy remain below; the
selection + rationale are recorded in the Selection subsection. The **two hi-fi finalists are
produced** (Option A — winner, and Option B — runner-up; see [Tier 2](#tier-2--high-fidelity-finalists-cost-of-living)
below) — neither is deferred. The full
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
funnel (diverge → narrow → select → justify) is satisfied across both the low-fi and hi-fi tiers.

**Prior art (R7)** — `web-researcher` surveyed comparable cost-of-living tools: **Numbeo**
(sortable ranked index + per-city category breakdown), **Expatistan** (two-city category breakdown),
**Nomad List** (filterable card grid + cost meters), **Numbeo cost-of-living estimator** (per-city
itemised monthly budget), **LivingCost.org** (per-city category bars). The proven multi-city scan
layouts are the **sortable category table** (Numbeo) and the **card grid** (Nomad List); the proven
drill-down idiom is the **itemised category breakdown** (Expatistan / Numbeo estimator). This
directly informs the three alternatives below.

**Grounding (R5)** — reuses `libs/web-ui`: `tabs` (Cost of living / Savings / Minimum role toggle),
`label`, `dropdown-menu`/`command` (the Region / Country / City cascading filters + household
selectors), `card`, `badge`, `button`. One **net-new primitive — `Table`** — is required (no `table`
component exists in `libs/web-ui`; see delivery Phase 2). The cascading filters reuse the existing
`command`/`dropdown-menu` combobox.

### Tier 1 — Low-Fidelity Alternatives (diverge)

Three genuinely different layouts (full ASCII in
[`assets/ui-cost-of-living-low-fi-alternatives.md`](./assets/ui-cost-of-living-low-fi-alternatives.md)):

```
Option A — Category Table (SELECTED)   Option B — Category Cards   Option C — Country Drill
┌──────────────────────────────────┐   ┌──────────┐ ┌──────────┐  ┌──────────┬─────────────┐
│ Country City  Hous … Schl  Total │    │ Jakarta  │ │ K.Lumpur │  │ Region   │ Jakarta, ID │
│ Indon.  Jkt·  600  …  0    $1,450│    │ Ess $1.2k│ │ Ess $1.4k│  │ Country  │ Hous   $600 │
│ Malays. KL·   720  …  0    $1,700│    │ Total1.4k│ │ Total1.7k│  │ [ID ▼ ]  │ Food   $250 │
│ Germany Berl· 1100 …  0    $2,600│    │ Reloc 4k │ │ Reloc 5k │  │ Jakarta  │ …    $1,450 │
│ (Country left of City; city name │    └──────────┘ └──────────┘  │ Bandung  │ Reloc  $4k  │
│  links to detail; sortable)      │    │ Berlin   │ │ Lisbon   │  └──────────┴─────────────┘
└──────────────────────────────────┘
```

### Selection — Option A (stakeholder-selected)

The stakeholder selected **Option A — Category Table**. Rationale: it is the densest worldwide-scan
layout (the Numbeo ranked-index idiom), keeps the full per-category breakdown inline for direct
cross-city comparison, and reflows cleanly to stacked cards on mobile; the card/drill alternatives show
too few cities for the worldwide scan. Refinements folded into Option A: the **Region / Country / City**
cascading filter row, a **Country column immediately left of City**, **city-name links** to the
single-city Cost-of-living **detail** view, and the **school** column shown inline. The selected
Option A is realised as a hi-fi finalist in [Tier 2](#tier-2--high-fidelity-finalists-cost-of-living) below.
Full rationale table + the city-detail sketch are in
[`assets/ui-cost-of-living-low-fi-alternatives.md`](./assets/ui-cost-of-living-low-fi-alternatives.md).

The Cost-of-living table columns are: **Country | City | Housing | Food | Transport | Utilities |
Healthcare (OOP) + scheme badge | Childcare | School | Essentials subtotal | Lifestyle | Monthly total |
Relocation sunk | Liquidity reserve | confidence**. Filters sit above; the city name links to the
single-city detail. The **Healthcare (OOP)** column header is accompanied by an **on-screen
explanation** that **OOP = out-of-pocket** — the healthcare costs the user pays themselves, on top of
any tax-funded or insurance coverage — shown as a legend/footnote line on the screen (and repeated in
the city-detail healthcare panel). This OOP explanation appears on **every tab that shows the Healthcare
(OOP) column**.

### Tier 2 — High-Fidelity Finalists (Cost of Living)

The narrow stage carries the **two strongest alternatives** forward in hi-fi: the selected
**Option A — Category Table** (winner) and the runner-up **Option B — Category Cards**. Drop reason
for Option C: single-country drill-down pane is too narrow for the worldwide scan and the left rail
stacks awkwardly on mobile — carried to hi-fi. Drop reason for Option B (runner-up):
card grid shows too few cities per screen for the worldwide scan and weakens side-by-side category
comparison — documented below.

#### Finalist 1 — Option A (Category Table) — SELECTED

The desktop high-fidelity finalist for the selected **Option A — Category Table**, with all current
refinements applied (three-tab toggle with Cost of living active; the Region / Country / City cascading
filter row; the household, area, and school-type controls; underlined city-name links; the always-on
healthcare funding-scheme badge **whose full label fits inside the taller table row**; an **OOP =
out-of-pocket legend line**; dual-currency money cells; the snapshot-date + "estimates only"
disclaimer; and a city-detail inset). Authored as an SVG and rasterised to PNG at 2× via
`rsvg-convert -z 2`, using the color-blind-friendly palette and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

![High-fidelity desktop mockup of the Cost-of-living tab as a Category Table: the three-tab toggle shows Cost of living active; a Region/Country/City cascading filter row and household, area, and school-type controls sit above a dense table whose rows (Jakarta Indonesia, Singapore, Berlin Germany) list each expense category with money cells showing local currency over USD and a healthcare funding-scheme badge per row whose full label sits inside the taller row, underlined Country and City links (a City link opens that city's detail, a Country link opens the Cost-of-living tab filtered to that country), a legend explaining OOP means out-of-pocket, and a city-detail inset plus an estimates-only disclaimer.](./assets/ui-cost-of-living-option-a-category-table.png)

#### Finalist 2 — Option B (Category Cards) — Runner-up

The desktop high-fidelity finalist for the runner-up **Option B — Category Cards**: each city is
rendered as a card with expense categories stacked, an essentials subtotal, a monthly total, a
relocation sunk-cost line, and a liquidity-reserve line. The three-tab toggle shows Cost of living
active; Region/Country/City cascading filters and shared household/area/school controls sit above
the card grid; healthcare funding-scheme badges are present per card; OOP legend shown. Authored as
an SVG and rasterised to PNG at 2× via `rsvg-convert -z 2`, using the color-blind-friendly palette
and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

**Drop reason**: card grid is more visual but shows too few cities per screen for the worldwide scan;
side-by-side category comparison is weaker than the inline table.

![High-fidelity desktop mockup of the Cost-of-living tab as a Category Cards layout (runner-up finalist): a three-tab toggle shows Cost of living active; Region/Country/City cascading filters and shared household/area/school controls sit above a grid of four city cards (Jakarta Indonesia, K. Lumpur Malaysia, Berlin Germany, Lisbon Portugal); each card lists all expense categories stacked with an essentials subtotal, a monthly total, a relocation sunk-cost line, and a liquidity-reserve line; healthcare funding-scheme badges are shown per card; an OOP legend and an estimates-only disclaimer appear below the grid; a dashed note explains why this design was dropped in favour of Option A.](./assets/ui-cost-of-living-option-b-category-cards.png)

### Responsive Design — Mobile / Tablet / Desktop

Designed **mobile-first**; the chosen category table reflows across the convention's three display
classes:

| Class   | Breakpoint       | Layout                                                                                                                                                                                                 |
| ------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Mobile  | base (`< sm`)    | Controls (household, area, Region/Country/City filters) stack full-width; each city renders as a **stacked card** headed "City, Country" (category rows, essentials subtotal, total, relocation line). |
| Tablet  | `md` (≥ 768 px)  | Controls in a 2-column grid; condensed table showing Country · City · Essentials · Total · Relocation, with the category columns revealed on row-expand/tap.                                           |
| Desktop | `lg` (≥ 1024 px) | Full category table with all category columns inline (Country left of City) plus subtotal, total, and relocation columns; controls in a single row.                                                    |

The selected Option A is delivered as a hi-fi finalist at **all three display sizes** (mobile, tablet,
desktop) — three of the **nine** hi-fi mockups across the three tabs. Desktop is the
[Finalist 1 above](#finalist-1--option-a-category-table--selected); the mobile and tablet finalists:

**Mobile (`< sm`) — stacked cards:**

![High-fidelity mobile mockup of the Cost-of-living tab: a narrow single-column phone layout with the three-tab toggle (Cost of living active), stacked Region/Country/City filters and household/area/school controls, and one city rendered as a stacked card headed "Jakarta, Indonesia" (underlined links) listing each expense category with local-over-USD values, a healthcare funding-scheme badge, an essentials subtotal, a monthly total, and a relocation line, the top edge of a second city card to imply scroll, an OOP = out-of-pocket legend, and an estimates-only disclaimer.](./assets/ui-cost-of-living-option-a-category-table-mobile.png)

**Tablet (`md`) — condensed table:**

![High-fidelity tablet mockup of the Cost-of-living tab: a 768px layout with controls in a two-column grid above a condensed table (Country, City, Scheme, Essentials, Total, Relocation) for Jakarta, Singapore, and Berlin with a tap-to-expand chevron that reveals the category columns, dual-currency cells, healthcare funding-scheme badges, underlined Country/City links, an OOP legend, and an estimates-only disclaimer.](./assets/ui-cost-of-living-option-a-category-table-tablet.png)

Low-fidelity reflow (mobile stacked-card vs desktop table) is sketched in the
[low-fi alternatives asset](./assets/ui-cost-of-living-low-fi-alternatives.md).

## UI Design — Savings Screen (Design Funnel)

The stakeholder has **selected Option A — Net/Savings Table** from the low-fidelity alternatives. The
low-fi ASCII alternatives (≥2) and a mobile/tablet/desktop responsive strategy remain below; the
selection + rationale are recorded in the Selection subsection. The **two hi-fi finalists are
produced** (Option A — winner, and Option B — runner-up; see [Tier 2](#tier-2--high-fidelity-finalists-savings)
below) — neither is deferred. The full
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
funnel (diverge → narrow → select → justify) is satisfied across both the low-fi and hi-fi tiers.

**Prior art (R7)** — `web-researcher` surveyed forward salary-to-savings tooling: **Numbeo
International Salary Equivalent** (salary in city A → equivalent net-preserving salary in city B),
**NerdWallet / Bankrate cost-of-living calculators** (two-city net-equivalence), **LivingCost.org**
(salary input + ranked savings cards), **levels.fyi** (gross compensation, no net/savings ranking).
**No tool ships "one gross salary → cities ranked by net-of-tax monthly savings" as a first-class
screen** — so the layout borrows the proven ranked-table idiom (Numbeo) personalised to a gross
salary with explicit net and savings columns.

**Grounding (R5)** — reuses `libs/web-ui`: `tabs` (tab toggle), `input` (gross salary monthly +
annual), `label`, `dropdown-menu`/`command` (Region / Country / City filters + household selectors),
`card`, `badge` (savings sign, confidence tier, non-salary-comp note, "Roles: software-engineering
(IC + management)" caption), `button`, and the **net-new `Table`** primitive (shared with
Cost-of-living and Minimum-role; see delivery Phase 2). No further net-new component is required for
this screen.

### Tier 1 — Low-Fidelity Alternatives (diverge)

Two genuinely different layouts (full ASCII in
[`assets/ui-savings-low-fi-alternatives.md`](./assets/ui-savings-low-fi-alternatives.md)):

```
Option A — Net/Savings Table (SELECTED)               Option B — Savings Card Grid
┌────────────────────────────────────────────────┐   ┌──────────┐ ┌──────────┐
│ Gross [ 8,000/mo ] (= 96,000/yr)               │   │ Jakarta,ID│ │ KL, MY   │
│ Cntry City  Gross/yr NonSal Tax% Net   Save  % │   │ Net $6.8k │ │ Net $6.5k│
│ ID    Jkt·  $96,000  +$10k 15% $6,800 $5,400 79│   │ +$10k RSU │ │ +$8k RSU │
│ MY    KL·   $96,000  +$8k  19% $6,500 $4,835 74│   │ Save5.4k  │ │ Save4.8k │
│ DE    Berl· $96,000  +$6k  35% $5,200 $2,680 52│   └──────────┘ └──────────┘
│ (Cntry left of City; city links to detail;     │   │ Lisbon,PT│ │ Berlin,DE│
│  NonSal = info only, not in savings; sortable) │   └──────────┘ └──────────┘
└────────────────────────────────────────────────┘
```

### Selection — Option A (stakeholder-selected)

The stakeholder selected **Option A — Net/Savings Table**. Rationale: it makes the gross → net →
essentials → savings chain transparent in one row across many cities (the Numbeo ranked-table idiom),
with room for the dual gross (monthly + annual), the non-salary-comp column, and the Country+City
columns; the card grid hides the net/essentials chain and shows too few cities for the worldwide scan.
Refinements folded into Option A: the **Region / Country / City** cascading filters, a **Country column
immediately left of City** + city-name links to the detail view, gross shown **monthly AND annual**, a
**non-salary comp** column (informational total-comp only), and a **"Roles: software-engineering
(IC + management)"** caption. The selected Option A is realised as hi-fi Finalist 1 in
[Tier 2](#tier-2--high-fidelity-finalists-savings) below.

The Savings table columns are: **Country | City | Gross (monthly + annual) | Non-salary comp | Total
comp (base + non-salary, informational) | Income band | Effective tax % (federal + sub-national) |
Net | Essentials | Lifestyle | Essential savings | After-lifestyle savings | Essential savings % |
healthcare scheme badge**. Sortable by essential savings; filters above; city name links to the
detail.

### Tier 2 — High-Fidelity Finalists (Savings)

The narrow stage carries the **two strongest alternatives** forward in hi-fi: the selected
**Option A — Net/Savings Table** (winner) and the runner-up **Option B — Savings Card Grid**. Drop
reason for Option B (runner-up): card grid hides the essentials/net chain and shows too few cities
per screen for the worldwide savings scan — documented below.

#### Finalist 1 — Option A (Net/Savings Table) — SELECTED

The desktop high-fidelity finalist for the selected **Option A — Net/Savings Table**, with all current
refinements applied (three-tab toggle with Savings active; the gross-salary input shown **monthly AND
annual**; the Region / Country / City cascading filters; the **shared cost-basis controls row —
household (adults, pre-school kids, school-age kids), area (center / rural), and school-type (public /
private)** — the same control set shown on every tab; the "Roles: software-engineering (IC +
management)" caption; the sortable-by-essential-savings indicator on that column; effective tax split
into federal + sub-national; non-salary comp marked informational; dual-currency money cells; underlined
city-name links; **healthcare scheme badges whose full label fits inside the row**; an **OOP =
out-of-pocket legend line**; and the "savings before pension" + "nominal-FX vs PPP" disclaimer).
Authored as an SVG and rasterised to PNG at 2× via `rsvg-convert -z 2`, using the
color-blind-friendly palette and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

![High-fidelity desktop mockup of the Savings tab as a Net/Savings Table: the three-tab toggle shows Savings active; a gross-salary input reads $8,000/mo equals $96,000/yr beside Region/Country/City filters, a roles caption, and a shared cost-basis controls row with household (adults, pre-school kids, school-age kids), area (center/rural), and school-type (public/private) controls; the table ranks Jakarta, Kuala Lumpur, and Berlin by essential savings (the sorted column highlighted) with columns for gross, non-salary comp, total comp, income band, effective tax split federal plus sub-national, net, essentials, lifestyle, essential and after-lifestyle savings, savings percent, and a healthcare scheme badge whose full label sits inside the row, money cells showing local over USD, both Country and City names rendered as underlined links (a City link opens that city's Cost-of-living detail, a Country link opens the Cost-of-living tab filtered to that country), a legend noting OOP means out-of-pocket, and a savings-before-pension and nominal-FX-vs-PPP disclaimer.](./assets/ui-savings-option-a-net-savings-table.png)

#### Finalist 2 — Option B (Savings Card Grid) — Runner-up

The desktop high-fidelity finalist for the runner-up **Option B — Savings Card Grid**: each city is
rendered as a card showing its rank, net take-home, non-salary comp line, essentials, essential and
after-lifestyle savings with percentages, and a healthcare scheme badge. Cards are ranked by essential
savings. The three-tab toggle shows Savings active; gross-salary input, Region/Country/City cascading
filters, and shared cost-basis controls sit above the card grid. Authored as an SVG and rasterised to
PNG at 2× via `rsvg-convert -z 2`, using the color-blind-friendly palette and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

**Drop reason**: card grid hides the gross→net→essentials→savings chain and shows too few cities per
screen for the worldwide savings scan; the transparent row-by-row chain of Option A is superior for
the tool's core use case.

![High-fidelity desktop mockup of the Savings tab as a Savings Card Grid (runner-up finalist): a three-tab toggle shows Savings active; a gross-salary input ($8,000/mo = $96,000/yr), Region/Country/City filters, and shared cost-basis controls sit above a 2x2 grid of ranked city cards; each card shows the rank number, underlined city and country links, a healthcare scheme badge, the net take-home, non-salary comp line, essentials, essential savings and percentage in teal, and after-lifestyle savings; cards are ordered Jakarta rank 1 (essential savings $5,400), K. Lumpur rank 2 ($4,835), Lisbon rank 3 ($3,320), Berlin rank 4 ($2,680); a legend notes OOP and that non-salary comp is informational; a dashed note explains why this design was dropped in favour of Option A.](./assets/ui-savings-option-b-savings-card-grid.png)

### Responsive Design — Mobile / Tablet / Desktop

Designed **mobile-first**; the chosen net/savings table reflows:

| Class   | Breakpoint       | Layout                                                                                                                                                                                                                                           |
| ------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Mobile  | base (`< sm`)    | Salary input (monthly + derived annual) + Region/Country/City filters + controls stack full-width; each city renders as a **stacked card** headed "City, Country" (net, non-salary comp, essentials, both savings, %), sort control as a select. |
| Tablet  | `md` (≥ 768 px)  | Controls in a 2-column grid; condensed table (Country · City · Net · Essential savings · %), the gross/annual + non-salary-comp columns revealed on row-expand/tap.                                                                              |
| Desktop | `lg` (≥ 1024 px) | Full table with Country+City, gross monthly+annual, non-salary comp, band + tax %, net, essentials, both savings, and % columns inline; controls in a single row.                                                                                |

The selected Option A is delivered as a hi-fi finalist at **all three display sizes** (mobile, tablet,
desktop). Desktop is the [Finalist 1 above](#finalist-1--option-a-netsavings-table--selected); the
mobile and tablet finalists:

**Mobile (`< sm`) — stacked cards:**

![High-fidelity mobile mockup of the Savings tab: a narrow single-column phone layout with the three-tab toggle (Savings active), a full-width gross-salary input ($8,000/mo = $96,000/yr), stacked Region/Country/City filters and cost-basis controls, and one city rendered as a stacked card headed "Jakarta, Indonesia" (underlined links) listing Gross, Non-salary comp, Total comp, Income band, Effective tax (federal + sub-national), Net, Essentials, Lifestyle, and the two highlighted savings figures with percentages and a healthcare scheme badge, the top edge of a second city card, an OOP legend, and a savings-before-pension / nominal-FX disclaimer.](./assets/ui-savings-option-a-net-savings-table-mobile.png)

**Tablet (`md`) — condensed table:**

![High-fidelity tablet mockup of the Savings tab: a 768px layout with controls in a two-column grid above a condensed table ranking Jakarta, Kuala Lumpur, and Berlin by essential savings (Country, City, Net, Essentials, Essential savings, After-lifestyle %, scheme badge) with a tap-to-expand chevron that reveals the gross/non-salary/total-comp/tax-split columns, dual-currency cells, underlined Country/City links, an OOP legend, and a disclaimer.](./assets/ui-savings-option-a-net-savings-table-tablet.png)

## UI Design — Minimum-Role Screen (Design Funnel)

The stakeholder has **selected Option A — Ladder Table** from the low-fidelity alternatives. The
low-fi ASCII alternatives (≥2) and a mobile/tablet/desktop responsive strategy remain below; the
selection + rationale are recorded in the Selection subsection. The **two hi-fi finalists are
produced** (Option A — winner, and Option B — runner-up; see [Tier 2](#tier-2--high-fidelity-finalists-minimum-role)
below) — neither is deferred. The full
[UI Mockups in Plan Docs convention](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
funnel (diverge → narrow → select → justify) is satisfied across both the low-fi and hi-fi tiers.

**Prior art (R7)** — `web-researcher` surveyed reverse salary/role tooling: **levels.fyi**
(forward role → salary; a compensation-range filter is the nearest reverse pattern but is not
city- or savings-aware), **Glassdoor / Payscale** (forward title + city → salary), **Numbeo
International Salary Equivalent** (salary in city A → equivalent salary in city B preserving net
savings; no role mapping), **NerdWallet / Bankrate** (US-only cost-of-living equivalence). **No tool
ships "one savings target → minimum role + city worldwide" as a first-class screen** — the feature is
novel, so the layout borrows the proven ranked-table idiom (Numbeo/levels.fyi) rather than copying a
specific competitor.

**Grounding (R5)** — reuses `libs/web-ui`: `tabs` (tab toggle), `input` (salary / savings target),
`label`, `dropdown-menu`/`command` (Region / Country / City filters, reference city/role,
display-currency, household selectors), `button` (pill/toggle buttons for the baseline-source selector
— My salary / Reference role / Savings target — and the area toggle — Center / Rural; no standalone
`RadioGroup` primitive exists in `libs/web-ui`; these controls are implemented as grouped `button`
elements styled as a segmented control, consistent with how the Area toggle is shown in all three
hi-fi mockups), `badge` (`MINIMUM` marker, confidence tier, "Roles: software-engineering (IC +
management)" caption, p25/median/p75 labels), `alert`/`InfoTip` (disclaimer), and the **net-new
`Table`** primitive (shared with the other tabs; see delivery Phase 2). No further net-new component
is required for this screen.

### Tier 1 — Low-Fidelity Alternatives (diverge)

Three genuinely different layouts (full ASCII in
[`assets/ui-min-role-low-fi-alternatives.md`](./assets/ui-min-role-low-fi-alternatives.md)):

```
Option A — Ladder Table (SELECTED, reordered)   Option B — Banner+List   Option C — Split
┌──────────────────────────────────────────┐    ┌──────────────────┐    ┌────────┬──────────┐
│ Roles: SWE (IC + mgmt)  bar = $2,100/mo   │    │ ┌──────────────┐ │    │Baseline│ Role  S  │
│ Role       Cntry Best  p25/med/p75 Save   │    │ │Min: Sr SWE   │ │    │(•)Ref  │ Dir  ✓   │
│ ── Qualifies ──────────────────────────── │    │ │Jakarta,ID    │ │    │Region▼ │ Staff✓   │
│ Director   MY  KL· $9/$12/$16k  $4,910 ✓  │    │ │$2.31k        │ │    │Cntry ▼ │ EM   ✓   │
│ Staff SWE  PH  Mnl·$6/$8/$11k   $3,520 ✓  │    │ └──────────────┘ │    │City  ▼ │ ▶SrSWE✓M │
│ ▶Sr SWE    ID  Jkt·$4/$6/$8k    $2,310✓MIN│    │ Qualifies:       │    │bar=$2k │ ──below──│
│ ── Below minimum ───────────────────────── │    │ • Staff Mnl $3.5k│    │Show  ▼ │ ░SWE II  │
│ ░ SWE II   ID  Jkt·$3/$4/$5k    $1,780     │    │ • Sr SWE Jkt←min │    │        │ ░SWE I   │
└──────────────────────────────────────────┘    └──────────────────┘    └────────┴──────────┘
```

### Selection — Option A (stakeholder-selected)

The stakeholder selected **Option A — Ladder Table**. Rationale: it shows the full ranked ladder with
the qualifying/non-qualifying split, the per-role best city + country, the p25/median/p75 distribution,
and the dual+ currencies in one dense, scannable surface (the levels.fyi/Numbeo ranked-table idiom);
the banner hides the near-miss context and the split-rail wastes width and forces awkward mobile
stacking. Refinements folded into Option A: (1) **reorder** so qualifying roles sit high→low down to the
marked MINIMUM, then a **divider**, then dimmed **non-qualifying ("below minimum")** roles; (2) a
**Country column** (best city + its country); (3) **p25 / median / p75** shown per role × country;
(4) a **non-salary comp** line; (5) **Region / Country / City** filters scope the candidate cities;
(6) a **"Roles: software-engineering (IC + management)"** caption; (7) city-name links to the detail.
The selected Option A is realised as hi-fi Finalist 1 in [Tier 2](#tier-2--high-fidelity-finalists-minimum-role) below.

The Minimum-role table columns are: **Role | Best city | Country | p25 | Median | p75 | Non-salary comp
| Total comp (base + non-salary, informational) | Essential savings** with a ✓/MINIMUM marker. **Every
money column — p25, median, p75, non-salary comp, total comp, and essential savings — is rendered dual:
the display currency on line 1 and the best city's local currency on line 2** (the display-currency
selector chooses line 1, defaulting to USD), consistent with the universal "local + USD everywhere"
rule. The ladder is **reordered**: qualifying roles grouped high→low down to the MINIMUM, a divider,
then the dimmed non-qualifying roles. Filters and the **shared household / area / school-type cost-basis
controls** scope and shape the candidate cities; ranking and the reference-role baseline use the
**median** salary as the representative figure, and the essential-savings figure uses the active
household / area / school basis.

### Tier 2 — High-Fidelity Finalists (Minimum Role)

The narrow stage carries the **two strongest alternatives** forward in hi-fi: the selected
**Option A — Ladder Table** (winner) and the runner-up **Option B — Banner + List**. Drop reasons for
Options B and C at the narrow stage: Option B hides the near-miss context (how close the failing rungs
came to qualifying); Option C left rail wastes width and forces awkward mobile stacking.

#### Finalist 1 — Option A (Ladder Table) — SELECTED

The desktop high-fidelity finalist for the selected **Option A — Ladder Table**, with all current
refinements applied (three-tab toggle with Minimum role active; the "Roles: software-engineering
(IC + management)" caption badge; the baseline selector — my salary / reference role / savings target —
plus the display-currency selector; the Region / Country / City scope filters; the **shared cost-basis
controls row — household (adults, pre-school kids, school-age kids), area (center / rural), and
school-type (public / private)** — the same control set shown on every tab; the p25 / median / p75
distribution per role × country; the non-salary-comp and total-comp columns; **every money column shown
dual (display currency on line 1 + local currency on line 2)**; qualifying roles ranked high→low down to
a clearly-marked **MINIMUM** row, then a divider, then the dimmed below-minimum roles; and the
disclaimer line). Authored as an SVG and rasterised to PNG at 2× via `rsvg-convert -z 2`, using the
color-blind-friendly palette and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

![High-fidelity desktop mockup of the Minimum-role tab as a Ladder Table: the three-tab toggle shows Minimum role active beside a software-engineering roles caption; a baseline selector (reference role chosen), a USD-default display-currency selector, Region/Country/City scope filters, and a shared cost-basis controls row with household (adults, pre-school kids, school-age kids), area (center/rural), and school-type (public/private) controls sit above the ladder; qualifying roles (Director, Staff SWE) are ranked high to low down to a highlighted Sr SWE MINIMUM row badged MIN, followed by a dashed Below Minimum divider and dimmed SWE II and SWE I rows; every money column (p25, median, p75, non-salary comp, total comp, essential savings) shows the display currency over the local currency, best-city and country are both underlined links (a best-city link opens that city's Cost-of-living detail, a country link opens the Cost-of-living tab filtered to that country), and a legend notes the minimum depends on the household/area cost basis above an estimates-only disclaimer.](./assets/ui-min-role-option-a-ladder-table.png)

#### Finalist 2 — Option B (Banner + List) — Runner-up

The desktop high-fidelity finalist for the runner-up **Option B — Banner + List**: a large answer
banner states the minimum role and city plainly at the top; below it a qualifying list shows all
role-city combinations sorted by essential savings, then a below-minimum section. Baseline selector,
display-currency selector, Region/Country/City scope filters, and shared cost-basis controls sit above
the banner. Authored as an SVG and rasterised to PNG at 2× via `rsvg-convert -z 2`, using the
color-blind-friendly palette and WCAG-AA contrast per the
[Diagrams convention](../../../repo-governance/conventions/formatting/diagrams/mermaid-color-accessibility-palette.md#accessible-color-palette).

**Drop reason**: the banner gives the plain answer directly but hides near-miss context — how close
failing rungs came to qualifying. The Ladder Table (Option A) surfaces the full qualifying/non-qualifying
ranked ladder with p25/median/p75 per role, which is the tool's core differentiator.

![High-fidelity desktop mockup of the Minimum-role tab as a Banner + List layout (runner-up finalist): the three-tab toggle shows Minimum role active; a baseline selector (Reference role chosen), display-currency selector, Region/Country/City filters, and shared cost-basis controls sit above a large blue answer banner reading Minimum role to match $2,100/mo essential savings: Senior SWE in Jakarta Indonesia, with median salary and savings details; below the banner a qualifying list ranks Staff SWE, Eng. Manager, and Sr SWE (highlighted as MIN) by essential savings with p25/median/p75 and non-salary-comp columns; a dashed below-minimum section shows SWE II and SWE I; a legend and disclaimer appear at the bottom; a dashed note explains why this design was dropped in favour of Option A.](./assets/ui-min-role-option-b-banner-list.png)

### Responsive Design — Mobile / Tablet / Desktop

Designed **mobile-first**; the chosen ladder table reflows across the convention's three display
classes:

| Class   | Breakpoint       | Layout                                                                                                                                                                                                                                                                                                                         |
| ------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Mobile  | base (`< sm`)    | Baseline + Region/Country/City controls stack full-width; the ladder renders as **stacked cards** headed "City, Country" (role title, country, p25/median/p75, savings in the three currencies, ✓/below badge), grouped into a qualifying group then a divider then the dimmed below-minimum group, threshold card emphasised. |
| Tablet  | `md` (≥ 768 px)  | Baseline controls in a 2-column grid; ladder as a condensed table (Role · Country · Best city · Savings(USD) · badge), p25/median/p75 + local/display currency shown on tap/row-expand; groups kept.                                                                                                                           |
| Desktop | `lg` (≥ 1024 px) | Full reordered ladder table with the Country column, p25/median/p75, non-salary comp, and all three currency columns inline; baseline controls in a single row.                                                                                                                                                                |

The selected Option A is delivered as a hi-fi finalist at **all three display sizes** (mobile, tablet,
desktop) — completing the **nine** hi-fi mockups across the three tabs. Desktop is the
[Finalist 1 above](#finalist-1--option-a-ladder-table--selected); the mobile and tablet finalists:

**Mobile (`< sm`) — stacked rank cards:**

![High-fidelity mobile mockup of the Minimum-role tab: a narrow single-column phone layout with the three-tab toggle (Minimum role active) and software-engineering-roles caption, stacked baseline and USD-default display-currency selectors, stacked scope filters and cost-basis controls, and the ladder rendered as stacked rank cards (Director, Staff SWE, a highlighted Sr SWE MIN card, a dashed Below-Minimum divider, then dimmed SWE II and SWE I cards); each card shows the role, best city and country as underlined links, and the p25/median/p75/non-salary-comp/total-comp/essential-savings money rows as display currency (USD) over local currency, above a legend and an estimates-only disclaimer.](./assets/ui-min-role-option-a-ladder-table-mobile.png)

**Tablet (`md`) — condensed ladder table:**

![High-fidelity tablet mockup of the Minimum-role tab: a 768px layout with selectors and cost-basis controls in a two-column grid above a condensed ladder table (Role, Best city with Country, Median, Essential savings, Status) with the Sr SWE minimum row highlighted and badged MIN, a dashed Below-Minimum divider with dimmed rows, and a tap-to-expand chevron revealing the p25/p75/non-salary/total-comp columns; money cells show display currency over local, with underlined best-city and country links, a legend, and a disclaimer.](./assets/ui-min-role-option-a-ladder-table-tablet.png)

Low-fidelity reflow (mobile stacked-card vs desktop table) is sketched in the
[low-fi alternatives asset](./assets/ui-min-role-low-fi-alternatives.md). Each low-fi alternative was
sketched mobile-first — the row→card collapse pattern is cleaner than a left-rail layout, a signal to
carry into the deferred selection.

## Savings Model (v1)

The model is a **net-of-tax, expense-composition** model. There are no rule-of-thumb budgeting
percentages anywhere (no 50/30/20, no "housing ≤ 35%", no percent-of-take-home ranges) — every number
is a modeled dataset expense.

### Currency display

**Every monetary figure is always shown in BOTH the city's local currency AND USD**, across all three
tabs — costs, the essentials subtotal and total, savings, net take-home, relocation, role salaries,
and the baseline. Neither currency is ever shown alone. On the **Minimum-role** tab the
**display-currency selector defaults to USD**, so by default every money figure (p25, median, p75,
non-salary comp, total comp, essential savings) reads as **USD + local** — just like the other tabs —
and the selector lets the user optionally switch the non-local line to another currency (e.g. EUR),
giving _chosen + local_. USD is the common unit for all absolute cross-city comparisons (see
Minimum-Role Resolution); the local and display-currency figures are presentation only.

**FX is single-sourced from `fx.ts`** — every currency conversion (local → USD, and USD → the chosen
display currency on the Minimum-role tab) reads from the in-repo `fx.ts` table (ISO-4217 → USD per 1
unit) with a recorded `fxSnapshotDate`. A city's `fxToUsd` is **derived** from `fx.ts` via the city's
`currency`, not hand-entered per city, so a currency's rate is stored exactly once.

### Expense composition (per city, monthly, curated/static)

Each city stores seven modeled monthly expense categories in local currency, each value
confidence-tiered (`high` | `moderate` | `proxy`) and snapshot-dated:

- **housing** — rent for a typical unit (scaled sub-linearly by household, discounted by area).
- **food** — groceries + eating out (scaled near per-capita by household).
- **transport** — a monthly **public-transit pass** (cars/fuel/parking are not modeled — fixed v1
  assumption, not a toggle).
- **utilities** — electricity, water, internet, mobile (scaled sub-linearly by household).
- **healthcare** — **out-of-pocket only** (scaled near per-capita). For `tax-funded`/`mixed` countries
  this is the small residual (prescriptions, dental, copays, optical), because mandatory health
  premiums already sit inside the country's effective tax + contribution rate (avoids double-counting);
  for `oop` countries it is the real out-of-pocket / private-insurance spend.
- **childcare** — median monthly cost **per pre-school child** (an essential, scaled near per-capita).
- **lifestyle** — discretionary (entertainment, fitness, misc.); **clothing and personal care are
  folded into lifestyle**, not separate categories.

Plus a per-**school-age-child** **school** median (`{ public, private }`).

The **essentials subtotal** = housing + food + transport + utilities + healthcare(OOP) + childcare +
school. The **total** = essentials + lifestyle.

Shared cost-basis controls scale the modeled categories on the OECD-modified equivalence basis (first
adult 1.0, +0.5 per extra adult, +0.3 per child):

- **household** (adults 1–2; pre-school children 0–3; school-age children 0–3) scales **housing +
  utilities sub-linearly** and **food + healthcare + childcare near per-capita**, adds **childcare**
  per pre-school child, and adds **schooling** per school-age child.
- **area** (`center` | `rural`) discounts mainly **housing** via the area-multiplier.
- **school type** (`public` | `private`) selects the per-school-age-child school median; shown only
  when there are school-age children.

### Gross salary: monthly and annual

The Savings tab accepts a **gross salary** as **either monthly or annual** (USD): the user enters one
field and the tool derives and shows the other (`annual = 12 × monthly`; `monthly = annual / 12`). Both
are displayed (an input pair plus a row/column in the results). The **monthly** USD figure is the one
fed into the income-band selection and the net-of-tax computation, so the math is unchanged — the
annual figure is presentation/entry convenience.

### Typical non-salary compensation (RSU / equity / bonus)

Per **role × country**, the dataset stores a typical **non-salary compensation** figure (typical annual
RSU/equity + bonus). It is **displayed as informational total-comp context** — a separate column/line
with a clear note — and is **NOT folded into the deterministic monthly net-savings math**. Both savings
figures (essential and after-lifestyle) are computed from **net base salary only**; non-salary comp
never enters them. The reason is **volatility**: RSU/equity value swings up and down with the share
price (and bonuses are not guaranteed), so folding it in would make the savings figure unstable and
unreliable for a relocation/negotiation decision. Equity vesting schedules and equity tax also stay out
of scope. "RSU/equity/bonus modeling into savings" therefore remains in Out of Scope; the field exists
only to give total-comp context alongside the gross base salary.

### Tax → net (federal banded rate + optional sub-national)

Each **country** stores a **federal** effective rate — combined income tax + mandatory contributions —
at a few monthly-income **bands** (`low` / `mid` / `high`). For **federal/multi-jurisdiction countries
(US states, Canada provinces, Switzerland cantons)** the **city** additionally stores a **sub-national**
banded effective rate, **added** to the federal rate. Unitary countries (UK, DE, JP, SG, Nordics, …)
have no sub-national component. For a gross salary, the tool picks the band and computes:

```
net = gross × (1 − (federalRate[band] + subNationalRate[band]))
```

(where `subNationalRate[band] = 0` for unitary countries). Each band rate is confidence-tiered and
snapshot-dated like every other cell. This is a deliberately simplified effective-rate model that
captures sub-national tax only for US/CA/CH; full progressive bracket engines, equity/RSU/bonus
handling, deduction optimization, filing status, benefits-in-kind, social-contribution caps, and
per-individual tax situations are out of scope.

### Savings (two figures, deterministic)

The Savings tab and the Minimum-role tab compute **two** savings figures, with essentials being
housing + food + transport + utilities + healthcare(OOP) + childcare + school:

```
essentialSavings      = net − essentials
afterLifestyleSavings = essentialSavings − lifestyle
```

(all categories after household/area/school adjustment; transport per the public-transit assumption).
**Both** figures are shown wherever savings appears (each in local + USD). Negative savings (essentials
exceed net) are shown explicitly. The **Minimum-role tab ranks roles on `essentialSavings`** converted
to **USD** (the common unit); **lifestyle is excluded from the ranking** because fixing lifestyle as a
modeled expense would bundle a personal-preference variable into an otherwise objective comparison.

### One-time relocation (separate, informational, split)

Per city, a one-time **relocation** figure is shown as its own line, kept **out of** the monthly
savings math (so monthly comparisons stay clean), and **split** into two parts grounded in
relocation-budgeting research:

- **Sunk costs** (money actually spent):
  - housing **deposit** (refundable, ≈ 1–3× monthly rent),
  - **key money** (NON-refundable, e.g. Japan _reikin_ ≈ 1–2× rent; 0 where not applicable),
  - **moving / shipping**,
  - **visa / admin** (cross-border only).
- **Liquidity reserve** (a reserve the user **keeps** — it transfers from origin savings to
  destination savings, NOT a sunk cost):
  - a **cash cushion** (≈ 3–6× essential monthly cost).

The liquidity reserve is shown **separately** and **clearly labelled**; it is **never folded into the
sunk-cost total or the monthly savings math**. Both parts are confidence-tiered and snapshot-dated.

### Per-tab math

Per city, with the modeled monthly categories (after household/area adjustment) in local currency,
`childcareLocal` = per-pre-school-child childcare median × pre-school children, `schoolLocal` =
per-school-age-child school median × school-age children, `fxToUsd` = USD value of 1 local-currency
unit (read from `fx.ts` via the city's `currency`), and
`effectiveRate[band] = country.effectiveRate[band] + (city.subNational?.effectiveRate[band] ?? 0)`:

- `essentialsLocal = housingLocal + foodLocal + transportLocal + utilitiesLocal + healthcareLocal + childcareLocal + schoolLocal`
- `expensesLocal = essentialsLocal + lifestyleLocal`
- `expensesUsd = expensesLocal × fxToUsd`
- **Cost of living** (no salary): show each category, `essentialsLocal`, `expensesLocal`,
  `expensesUsd`, the one-time `relocationSunkLocal` / `relocationSunkUsd`, and the separately labelled
  `liquidityReserveLocal` / `liquidityReserveUsd`.
- **Savings** (gross salary entered in USD): `netUsd = grossUsd × (1 − effectiveRate[band(grossUsd)])`;
  `essentialSavingsUsd = netUsd − essentialsUsd`; `afterLifestyleSavingsUsd = essentialSavingsUsd − lifestyleUsd`;
  each `…Pct = …SavingsUsd / netUsd × 100`.
- Deficit case (`essentials > net`) yields negative savings and percentage, shown explicitly.

Figures are estimates; the UI shows the **snapshot date** and an "estimates only" note.

### Minimum-Role Resolution (compare savings in absolute terms)

The minimum-role tab reuses the same per-city expense + tax model, then adds role salaries (a per-role
× **country** distribution) and a reverse search. Because candidates span many currencies, **all
absolute comparisons are done in USD** (the common unit), with local and a user-chosen display currency
shown alongside. **The ranking figure is `essentialSavings`** computed from the role × country
**median** salary (lifestyle excluded — see Savings above; non-salary comp excluded — informational
only); `afterLifestyleSavings` is shown for context only.

- **Candidate scope** — the active **Region / Country / City** filters define the candidate city set;
  each role's best city is chosen **within that filtered set** (no filter ⇒ all cities).
- **Baseline savings `B` (USD)** — resolved from the chosen baseline source (on `essentialSavings`):
  - _My salary_: `B = essentialSavingsUsd` of the entered gross salary (net-of-tax essential savings
    under the active cost basis).
  - _Reference role_: pick city `c` + role `r`;
    `B = savingsRow(c, grossUsd = roleMedianGrossUsd(c, r), opts).essentialSavingsUsd`, i.e. that
    role's net-of-tax essential savings in that city (using the role × country **median** salary)
    under the active cost basis.
  - _Savings target_: user types `T` in display currency `d`; `B = T × fxToUsd(d)`.
- **Role salary** — the role × **country** distribution `{ p25, median, p75 }` from `roles.ts`; cities
  inherit their country's distribution. The **median** is the representative figure:
  `roleMedianGrossUsd(c, r) = matrix.salaries[city(c).countryId][r].median.monthlyGrossLocal × city(c).fxToUsd`.
  p25/p75 and the non-salary comp are displayed but never enter the ranking.
- **Candidate savings** — for every `(city c, role r)` with `c` in the filtered scope,
  `cand(c, r) = savingsRow(c, roleMedianGrossUsd(c, r), opts).essentialSavingsUsd`, using the **same**
  household/area/school cost basis and the country's federal + city sub-national tax model.
- **Per-role best city** — for each role `r`, `bestCity(r) = argmax_c cand(c, r)` over the filtered
  scope; `bestSavings(r) = cand(bestCity(r), r)` (best **essential** savings); the row carries
  `bestCity(r)` **and its country**.
- **Qualifying** — role `r` _clears the bar_ when `bestSavings(r) >= B`.
- **Minimum role** — among qualifying roles, the one with the **lowest seniority rank**. Ties on rank
  break by higher `bestSavings`.
- **Display ordering (reordered around the minimum)** — the ladder is split into two groups:
  **qualifying** roles first, ordered by seniority **high → low** down to the marked MINIMUM qualifier;
  then a **divider**; then the **non-qualifying ("below minimum")** roles, **dimmed**. (Rank is a
  display/seniority ordering only; the qualifying test is purely the absolute-savings comparison — see
  `tech-docs.md` for the ordering rule across IC and management tracks.)
- **Edge cases** — if **no** role clears the bar, the UI says so explicitly rather than marking a
  row. Each candidate carries its cell **confidence tier**; low-confidence (`proxy`) winners are
  flagged.

## User Stories

### US-01: See the cost-of-living breakdown across cities

As a relocation planner, I want a table of tech-hub cities each showing its country and city, the full
monthly expense breakdown (housing, food, transport, utilities, healthcare, childcare, school,
lifestyle) with an essentials subtotal and a total, So that I can compare what it actually costs to
live in each hub.

### US-02: Filter cities by Region, then Country, then City

As a relocation planner, I want a cascading Region → Country → City filter on every tab (region narrows
the countries, country narrows the cities), So that I can scope the table from a whole region down to a
single city; every row always shows both the country and the city.

### US-14: Drill into a single city's full cost-of-living detail

As a relocation planner, I want to click any city name (on any tab) and land on a single-city
Cost-of-living detail view showing that city's full per-category breakdown, essentials subtotal, total,
healthcare scheme, and split relocation in local + USD, So that I can study one city in depth; I want
the view to be deep-linkable (`?tab=cost&city=<id>`) So that I can share it.

### US-17: Jump from a country name to that country's cities

As a relocation planner, I want to click any country name (on any tab) and land on the Cost-of-living
tab filtered to that country — its cities shown as a filtered list with the Country filter (and its
Region) pre-selected — So that I can scan all the cities in a country I'm interested in without manually
setting the cascading filters; I want the view to be deep-linkable (`?tab=cost&country=<id>`) So that I
can share it.

### US-03: See the one-time relocation budget, split sunk vs reserve

As a relocation planner, I want each city to show a separate one-time relocation **sunk-cost** total
(deposit, key money, moving, visa/admin) and a separately labelled **liquidity reserve** (the cash
cushion I keep), So that I can budget money actually spent apart from the reserve I retain, both apart
from monthly costs.

### US-04: Compare net-of-tax savings for my gross salary

As a tech worker, I want to enter my gross salary as either a **monthly or an annual** figure (seeing
both, annual = 12 × monthly) and see, per city, my net take-home after tax, my modeled essentials, and
**both savings figures** (savings after essentials, and savings after lifestyle) with their
percentages, So that I know where I keep the most.

### US-15: See typical non-salary compensation and total compensation as context

As a tech worker preparing a **salary negotiation**, I want each role/city's typical non-salary
compensation (RSU/equity + bonus) and a derived **total compensation** (base + non-salary comp) shown
as informational columns, clearly noted as **not** part of the net-savings math, So that I can
benchmark a real offer's whole package without the savings figure being distorted by equity I cannot
model deterministically.

### US-05: Understand the net-of-tax model

As a visitor, I want each savings row to show net (after the country's federal effective tax plus any
state/province/canton sub-national tax) separately from gross, So that I understand the figure is
net-of-tax, not gross-minus-cost.

### US-06: Adjust cost basis for household size

As a visitor with a family, I want to set the household as single/married plus counts of pre-school
and school-age children, So that the modeled expenses (housing + utilities sub-linearly, food +
healthcare + childcare near per-capita), childcare, and schooling — and therefore my savings — reflect
my situation.

### US-07: Choose public vs private schooling

As a visitor with school-age children, I want to toggle between public and private school, So that the
schooling portion of my expenses uses the median cost for the type I expect to use.

### US-13: See the healthcare funding scheme

As any visitor, I want every tab to always show the healthcare funding scheme for the selected
city/country (tax-funded / mandatory payroll insurance / out-of-pocket), So that I understand how
health cover is funded and why the healthcare expense models out-of-pocket costs only.

### US-08: Choose city-center vs rural living

As a visitor, I want to toggle between living in the city center and a rural/outer area, So that my
modeled housing-driven costs reflect where I'd actually live.

### US-09: Use the tool in Indonesian

As an Indonesian visitor, I want all labels, category names, tax/net wording, relocation labels, and
disclaimers in `id`, So that the tool is fully usable in my language.

### US-10: Understand data limits

As any visitor, I want a visible snapshot date, confidence flags on lower-quality cells, and an
"estimates only" disclaimer, So that I don't treat the figures as exact.

### US-11: Find the minimum software-engineering role for a savings bar

As a career planner, I want to set a savings baseline and see the **lowest software-engineering role**
(IC or management, anywhere in the world) whose typical (median) salary saves at least as much
net-of-tax **essential savings** (lifestyle excluded) in absolute terms, with the ladder **reordered**
so qualifying roles sit above the marked minimum and non-qualifying roles sit dimmed below a divider,
So that I know what seniority my goal implies on an objective basis.

### US-16: See the role-salary distribution per role and country

As a career planner, I want each role's salary shown as a **p25 / median / p75 distribution per role ×
country** (the median being the figure used for ranking), and to know the roles are
**software-engineering roles (IC + management)**, So that I understand the spread and read the ladder
in the right context rather than treating one number as the salary.

### US-12: Choose how the baseline is set and read savings in my currency

As a minimum-role user, I want to set the baseline three ways — my own salary, a reference city +
role, or a raw savings target — and read **every money figure (each salary percentile, each
compensation figure, and the savings)** in the candidate city's local currency and USD (always both),
with the display currency I pick on the primary line, So that the comparison fits whatever I already
know without any column hiding the local value.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: Salary savings calculator

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

  Scenario: Region narrows the country filter and country narrows the city filter
    Given I am on "/en/tools/cost-of-living-calculator"
    And the "Cost of living" tab is active
    When I select the region "ASEAN" then the country "Indonesia" in the cascading filters
    Then the Country filter lists only ASEAN countries
    And the City filter lists only Indonesian cities
    And only cities in Indonesia are shown in the table

  Scenario: Country and city are always shown together on every tab
    Given I am on "/en/tools/cost-of-living-calculator"
    When I view any tab's results table
    Then every row shows a Country column immediately to the left of the City column

  Scenario: Clicking a city name opens its single-city cost-of-living detail
    Given I am on "/en/tools/cost-of-living-calculator"
    When I click a city name in any table
    Then I am taken to that city's single-city Cost-of-living detail at "?tab=cost&city=<id>"
    And the City filter is pre-selected to that city
    And the detail shows the full per-category breakdown, essentials subtotal, total, healthcare scheme badge, and split relocation in both local currency and USD

  Scenario: Clicking a country opens Cost-of-living filtered to that country
    Given I am on "/en/tools/cost-of-living-calculator"
    When I click a country name in any table
    Then I am taken to the Cost-of-living tab filtered to that country at "?tab=cost&country=<id>"
    And the Country filter is pre-selected to that country with its Region set
    And the table shows that country's cities as a filtered list rather than a single-city detail

  Scenario: A city link takes precedence over a country link when both params are present
    Given I am on the calculator with both a country and a city query param set
    When the page resolves the deep link at "?tab=cost&country=<id>&city=<id>"
    Then the single-city Cost-of-living detail for the city is shown because a city implies its country

  Scenario: Healthcare funding scheme is always shown
    Given I am on "/en/tools/cost-of-living-calculator"
    When I select any city on any tab
    Then a healthcare funding-scheme badge is shown for that city's country
    And the badge reads "tax-funded", "mandatory payroll insurance", or "out-of-pocket"

  Scenario: The OOP abbreviation is explained on screen
    Given I am on a tab that shows the "Healthcare (OOP)" column
    When I read the legend near the table
    Then an on-screen explanation states that "OOP = out-of-pocket"
    And the explanation says it is the healthcare you pay yourself on top of any tax-funded or insurance coverage

  Scenario: Relocation reserve is shown separately from sunk costs
    Given I am on the "Cost of living" tab
    When I read a city row
    Then the one-time relocation sunk-cost total is shown distinct from the monthly total
    And the liquidity-reserve cash cushion is shown in its own labelled figure, not folded into the sunk-cost total

  Scenario: Savings tab converts gross salary to net before subtracting expenses
    Given I am on "/en/tools/cost-of-living-calculator"
    And I switch to the "Savings" tab
    When I enter a gross monthly salary of "8000" USD
    Then each city row shows a net take-home after the country's federal and sub-national effective tax
    And each row shows the essentials, the savings after essentials, and the savings after lifestyle with percentages
    And the table can be sorted by savings

  Scenario: Gross salary entered monthly shows the derived annual figure
    Given I am on the "Savings" tab
    When I enter a gross monthly salary of "8000" USD
    Then the annual gross is shown as "96000" USD
    And the annual figure equals twelve times the monthly figure

  Scenario: Non-salary comp is shown as informational context only
    Given I am on the "Savings" tab with a gross salary entered
    When I read a city row
    Then a typical non-salary compensation (RSU/equity + bonus) figure is shown as a separate informational column
    But it is not added into the net, the essential savings, or the after-lifestyle savings

  Scenario: Total compensation is shown for negotiation context
    Given I am on the "Savings" tab with a gross salary entered
    When I read a city row
    Then a total compensation figure equal to the base annual gross plus the typical non-salary comp is shown as informational context
    And the total compensation is not added into the net, the essential savings, or the after-lifestyle savings

  Scenario: Sub-national tax lowers net only in federal countries
    Given I am on the "Savings" tab with a gross salary entered
    When I compare a US, Canadian, or Swiss city against a unitary-country city
    Then the federal-country city applies its city sub-national rate on top of the federal rate
    But the unitary-country city applies the federal rate alone

  Scenario: Net take-home is lower than the entered gross
    Given I am on the "Savings" tab
    When I enter a gross monthly salary above a city's tax band threshold
    Then the net take-home shown for that city is lower than the entered gross

  Scenario: Essentials above net show a deficit
    Given I am on the "Savings" tab for a high-cost city
    When I enter a gross salary whose net is lower than that city's modeled essentials
    Then the savings-after-essentials amount and percentage are shown as negative

  Scenario: Indonesian locale is fully translated
    Given I am on "/id/tools/cost-of-living-calculator"
    When the page finishes loading
    Then all labels, category names, tax wording, healthcare-scheme labels, relocation labels, and the disclaimer are in Indonesian

  Scenario: No Israeli cities are listed
    Given I am on the calculator in either locale
    When the page finishes loading
    Then no Israeli city appears in the dataset or any table

  Scenario: Data snapshot date is clearly shown
    Given I am on the calculator
    When the page finishes loading
    Then I see a prominent "Data last updated" label with the dataset snapshot date
    And I see an "estimates only" disclaimer

  Scenario: Every monetary figure converts to USD via the in-repo FX table
    Given I am on the calculator
    When I read any USD figure derived from a local-currency value
    Then the conversion uses the rate for that currency stored in the in-repo fx.ts table
    And every currency referenced by a city, country, role, or display-currency selector has an fx.ts entry

  Scenario: Adding adults and children changes the modeled expenses
    Given I am on the "Cost of living" tab
    When I change the household from "single" to married with 2 school-age children
    Then the modeled housing and utilities increase sub-linearly
    And the modeled food and healthcare increase near per-capita
    And schooling is added for the two school-age children

  Scenario: Pre-school children incur childcare, not schooling
    Given I am on the "Cost of living" tab
    When I set the household to 1 pre-school child and 0 school-age children
    Then the childcare expense is added for the one pre-school child
    But no schooling cost is added

  Scenario: School type toggle is hidden without school-age children
    Given I am on "/en/tools/cost-of-living-calculator"
    When the household has no school-age children
    Then no school-type toggle is shown

  Scenario: Private school raises expenses more than public
    Given I am on "/en/tools/cost-of-living-calculator"
    And the household has 2 school-age children
    When I switch the school type from "public" to "private"
    Then the schooling portion of the modeled expenses increases

  Scenario: Rural area lowers housing versus city center
    Given I am on the "Cost of living" tab
    When I switch the area from "city center" to "rural"
    Then the modeled housing expense decreases
    And the city total decreases accordingly

  Scenario: Minimum role for a savings target ranks on essential savings and is reordered
    Given I am on "/en/tools/cost-of-living-calculator"
    And I switch to the "Minimum role" tab
    And I set the baseline source to "savings target"
    When I enter a monthly savings target of "8000" USD
    Then I see the software-engineering role ladder with qualifying roles grouped above a divider and non-qualifying roles dimmed below it
    And the lowest role whose best city reaches at least 8000 USD essential savings is marked as the minimum
    And roles whose best city cannot reach 8000 USD essential savings are shown below the divider and de-emphasised

  Scenario: Roles are labelled as software-engineering roles
    Given I am on the "Minimum role" tab
    When the page finishes loading
    Then a caption states the ladder is software-engineering roles covering IC and management tracks

  Scenario: Each role shows its per-country salary distribution
    Given I am on the "Minimum role" tab with a baseline set
    When I read a role row
    Then the role shows its country's p25, median, and p75 salary distribution
    And the row's essential savings is computed from the median salary

  Scenario: Best city shows its country alongside the city name
    Given I am on the "Minimum role" tab with a baseline set
    When I read a qualifying role row
    Then the row shows the best city and its country

  Scenario: Geographic filter scopes the candidate cities
    Given I am on the "Minimum role" tab with a baseline set
    When I select the country "Indonesia" in the cascading filters
    Then each role's best city is chosen only from Indonesian cities

  Scenario: Non-salary comp does not change the minimum-role ranking
    Given I am on the "Minimum role" tab with a baseline set
    When I compare two roles whose non-salary comp differs but whose median salary is equal
    Then their essential-savings ranking is unchanged because non-salary comp is informational only

  Scenario: Lifestyle does not change the minimum-role ranking
    Given I am on the "Minimum role" tab with a baseline set
    When I change a city's lifestyle assumption
    Then the marked minimum role is unchanged because ranking is on essential savings only

  Scenario: Minimum role from a reference city and role
    Given I am on the "Minimum role" tab
    And I set the baseline source to "reference role"
    And I pick the city "Jakarta" and the role "Senior SWE"
    When I view the minimum role result
    Then the baseline savings bar equals that role's essential savings in Jakarta
    And the marked minimum role reaches at least that essential savings in absolute terms

  Scenario: Minimum role from my own salary
    Given I am on the "Minimum role" tab
    And I set the baseline source to "my salary"
    When I enter my gross salary and its city
    Then the baseline savings bar equals my computed essential savings
    And the ladder marks the lowest role that meets or beats it

  Scenario: Savings shown in USD, local, and display currency
    Given I am on the "Minimum role" tab with a baseline set
    When I choose a display currency
    Then each role row shows its essential savings in USD, the city's local currency, and the display currency

  Scenario: Every money column on the Minimum-role tab is dual currency
    Given I am on the "Minimum role" tab with a baseline set and a display currency chosen
    When I read a role row
    Then every money column (p25, median, p75, non-salary comp, total comp, and essential savings) shows the display currency on the first line and the city's local currency on the second line
    And no money column shows only a single currency

  Scenario: Household composition changes the minimum qualifying role
    Given I am on the "Minimum role" tab and the "SWE I" role qualifies for the "single" household basis
    When I change the household to "married with 2 children" and the area to "center"
    Then "SWE I" no longer qualifies because childcare, schooling, and central housing raise its essentials above its net
    And a more senior role becomes the marked minimum

  Scenario: No role can reach the bar
    Given I am on the "Minimum role" tab
    When I set a savings target higher than any role's essential savings in any city
    Then the tool states that no role clears the bar
    And no row is marked as the minimum

  Scenario: Cost-basis controls affect role candidates
    Given I am on the "Minimum role" tab with a baseline set
    When I change the household type or area
    Then the role candidates' savings and the marked minimum role update accordingly

  Scenario: Low-confidence cells are flagged
    Given I am on the calculator
    When the page finishes loading
    Then any cell backed by a lower-confidence estimate shows a confidence flag

  Scenario: No Israeli city appears among role candidates
    Given I am on the "Minimum role" tab
    When the page finishes loading
    Then no Israeli city appears as a candidate city for any role
```

## Functional Requirements

- FR-1: Route `/[locale]/tools/cost-of-living-calculator` renders in `en` and `id` with three tabs (Cost of
  living, Savings, Minimum role).
- FR-2: **Cost of living** tab (no salary input): a table of all cities with a **Country column
  immediately to the left of the City column**, each row showing the seven modeled monthly expense
  categories (housing, food, transport, utilities, healthcare, **childcare**, lifestyle) plus the
  **school** add-on, an essentials subtotal, a total, a separate one-time relocation **sunk-cost**
  total, and a separately labelled **liquidity reserve**; sortable; each **city name is a link** to its
  single-city Cost-of-living detail and each **country name is a link** to the Cost-of-living tab
  filtered to that country.
- FR-2b: A shared **Region → Country → City** cascading filter group applies to all three tabs:
  selecting a Region narrows the Country list, selecting a Country narrows the City list, and each
  level is clearable (clearing a higher level resets the lower ones). It replaces the removed single
  country-only filter and the removed single-city mode.
- FR-2c: **Every table row on every tab always shows both Country and City** — a Country column
  immediately to the left of the City column (mobile cards read "City, Country") — and **both the
  Country name and the City name are clickable links** that navigate to the Cost-of-living tab with the
  related geographic filter pre-selected.
- FR-2d: **Clicking any city name anywhere** navigates to a single-city **Cost-of-living detail** view
  (the Cost-of-living tab scoped to that one city, with the City filter pre-selected) showing the full
  per-category breakdown, essentials subtotal, total, healthcare scheme badge, and split relocation
  (sunk + liquidity reserve), all in local + USD. The view is **deep-linkable** via `?tab=cost&city=<id>`
  and offers a back affordance.
- FR-2e: **Clicking any country name anywhere** navigates to the **Cost-of-living tab filtered to that
  country** — the Country filter (and its Region) pre-selected so the table shows that country's cities
  as a filtered list (NOT a single-city detail). The view is **deep-linkable** via
  `?tab=cost&country=<id>`. The page reads/writes the `tab`, `country`, and `city` query params; if both
  `country` and `city` are present, the `city` deep-link takes **precedence** (a city implies its
  country).
- FR-3: **Savings** tab: a gross salary input accepted as **monthly or annual** (enter one, both
  shown; annual = 12 × monthly), in USD → for each city, the Country+City, the gross monthly AND
  annual, a typical **non-salary comp** (RSU/equity + bonus) informational column, the income band +
  effective tax %, net take-home (via the country's federal banded effective tax rate plus any city
  sub-national rate), modeled essentials, **both savings figures** (`essentialSavings` and
  `afterLifestyleSavings`) with their percentages; sortable table.
- FR-3a: Net take-home is computed as
  `net = gross × (1 − (federalRate[band] + subNationalRate[band]))` where `band` is the income band
  the **monthly** gross falls into for that city's country, `federalRate` is the country's effective
  rate, and `subNationalRate` is the city's state/province/canton rate (0 for unitary countries).
- FR-3b: The gross salary is accepted as monthly OR annual and both are derived and displayed
  (`annual = 12 × monthly`, `monthly = annual / 12`); the monthly USD figure drives the tax band and
  the net computation.
- FR-3c: A typical **non-salary compensation** (annual RSU/equity + bonus) per role × country is
  **displayed as informational total-comp context only** and is **NOT** folded into net, essential
  savings, or after-lifestyle savings — both savings figures use net **base salary only**, because
  RSU/equity is **volatile** (swings with the share price; bonuses not guaranteed) and would otherwise
  destabilize the savings figure.
- FR-3d: The Savings tab surfaces a **total compensation** view for negotiation context — base
  (monthly + annual) plus the typical **non-salary comp** → **total annual compensation**
  (`totalComp = grossAnnual + nonSalaryComp.annual`), shown as an informational figure alongside the
  net/savings columns. Total comp is **informational only** and is **NOT** part of the net, the
  essential savings, or the after-lifestyle savings.
- FR-4: **Minimum role** tab: a baseline selector (my salary | reference role | savings target) →
  the **software-engineering** role ladder (IC + management; a caption states this), each role showing
  its best (cheapest-qualifying) city **and its country**, the role × country **p25 / median / p75**
  salary distribution, a typical **non-salary comp**, a derived **total compensation** (base +
  non-salary comp, informational, for negotiation context), and that best city's absolute **essential
  savings** (computed from the **median** salary; lifestyle excluded from the ranking), with the lowest
  qualifying role marked as the minimum; `afterLifestyleSavings` shown for context. The ladder is
  **reordered**: qualifying roles grouped high→low down to the marked MINIMUM, a divider, then dimmed
  **non-qualifying ("below minimum")** roles. The active Region/Country/City filters **scope the
  candidate cities**.
- FR-5: A household control (single/married = 1–2 adults; counts of pre-school children 0–3 and
  school-age children 0–3) applies to all three tabs; it scales modeled expenses on the OECD-modified
  basis (housing + utilities sub-linearly; food + healthcare + childcare near per-capita), adds
  childcare per pre-school child, and adds schooling per school-age child; all figures (including role
  candidates) recompute from it.
- FR-6: When the household has school-age children, a school-type toggle (`public` | `private`)
  applies; the chosen type's **median** per-school-age-child school cost is added per school-age child.
  The toggle is hidden when there are no school-age children.
- FR-7: An area toggle (`center` | `rural`) applies to all three tabs; `rural` discounts mainly
  housing via a shared area-multiplier. Area affects the modeled categories only, not childcare or
  schooling.
- FR-8: Currency and number formatting respect each city's currency and the active locale; **every**
  monetary figure across all three tabs — expenses, the essentials subtotal and total, both savings
  figures, net take-home, relocation sunk costs, the liquidity reserve, role salaries, and the
  baseline — is shown in **both** the city's local currency **and** USD (never either alone). The
  minimum-role tab additionally shows its user-chosen display currency (local + USD + chosen).
- FR-8a: **All currency conversion uses the in-repo `fx.ts` table as its single source.** `fx.ts`
  maps each ISO-4217 currency code → USD value per 1 unit and records a `fxSnapshotDate`; every
  conversion in the app (local → USD, and USD → the chosen display currency) reads from it. A city's
  `fxToUsd` is **derived** from `fx.ts` via the city's `currency`, not stored as a standalone
  hand-entered field. Every currency used by any city/country/role and every supported chosen-display
  currency must have an `fx.ts` entry.
- FR-9: Negative (deficit) savings (both figures) are computed and displayed explicitly.
- FR-10: The dataset excludes all Israeli cities and records a snapshot date. The exclusion is a
  deliberate country-level choice about the state of Israel and its political stance — **not** about
  any ethnic, racial, or religious group.
- FR-11: Visible **Disclaimers** subsection (see Disclaimers below) covering at minimum: "estimates
  only"; "savings are net of a **simplified effective tax rate** (federal + sub-national for US/CA/CH
  only) — not a full bracket calculation, and excluding filing status, deductions, benefits-in-kind,
  and social-contribution caps"; "household and rural costs are derived from shared OECD-modified
  multipliers and childcare/school costs are city medians — not exact per-case data"; "transport
  assumes public transport (monthly pass); car ownership is not modeled"; "relocation sunk costs are a
  one-time estimate kept out of the monthly savings math, and the cash cushion is a reserve you keep,
  not a sunk cost"; "savings are **before** any voluntary pension/retirement contributions"; "clothing
  and personal care are folded into lifestyle"; "a positive USD savings figure does **not** mean equal
  purchasing power — USD uses a nominal FX snapshot, not PPP"; and "healthcare models out-of-pocket
  costs only; the funding scheme is shown per country". Salary input labels read "Gross monthly salary
  (before tax)".
- FR-12: The page **clearly and prominently shows when the data was last fetched/updated** — a "Data
  last updated: &lt;date&gt;" label (localized, from the dataset `snapshotDate`) placed near the
  results.
- FR-13: The baseline savings bar is **normalised to USD** for the qualifying comparison; a role
  "clears the bar" when its best-city (within the filtered scope) absolute **essential savings** (USD),
  computed from the role × country **median** salary, is ≥ the baseline (USD). The "minimum" is the
  lowest-seniority qualifying role; if none qualifies, the UI says so. The ladder is **reordered** so
  qualifying roles are grouped above the marked minimum and non-qualifying roles are grouped, dimmed,
  below a divider.
- FR-14: The baseline can be set three ways — (a) my salary (+ its city/country), (b) a reference
  city + software-engineering role (using the role × country **median** salary), (c) a raw savings
  target in a chosen currency — and switching source recomputes the ladder.
- FR-15: In minimum-role mode **every money column on each role row — p25, median, p75, non-salary
  comp, total comp, and essential savings — is shown dual: the candidate city's local currency AND the
  display currency (which defaults to USD), never a single currency**; a display-currency selector
  chooses the primary line. This makes the percentile and compensation columns dual just like essential
  savings, consistent with the universal "local + USD everywhere" rule (NFR-1e).
- FR-16: Each city carries seven modeled expense categories (incl. `childcare`), a
  `childcareMedianLocal`, a `{ public, private }` school median, a split one-time relocation block
  (sunk costs incl. **key money** + a liquidity-reserve cash cushion), an ISO-4217 `currency` (its
  FX-to-USD rate is **derived from `fx.ts`**, not stored on the city), and — for US/CA/CH cities — a
  `subNational` banded effective rate; each country carries federal banded effective tax rates and a
  `healthcareModelType`. Every modeled cell carries a confidence tier (`high` | `moderate` | `proxy`)
  and rows backed by `proxy`/`moderate` data are visibly flagged.
- FR-17: The role-salary matrix (`roles.ts`) is keyed **per role × country** and stores a
  **`{ p25, median, p75 }`** gross-salary distribution (each confidence-tiered) plus a typical
  **non-salary comp** (annual RSU/equity + bonus) per role × country; cities **inherit** their
  country's distribution (role salary is national-level — a documented simplification). It excludes
  Israeli countries/cities, records a salary `snapshotDate`, and carries per-cell confidence tiers.
- FR-17a: The roles in the ladder are **software-engineering roles** spanning the **IC and management**
  tracks; every role-showing surface displays a caption/badge stating "Roles: software-engineering
  (IC + management)".
- FR-18: Each country carries a `compulsoryInsurance` record (whether health insurance is a legal
  necessity and whether pension/social/unemployment contributions are mandatory). The UI surfaces a
  per-country **"health insurance: compulsory / optional"** indicator (and, where relevant, a
  mandatory-social-contributions note) on the Cost-of-living tab (and per city on the other tabs).
  Where a mandatory health premium is payroll-deducted inside the country's effective tax rate, the
  `healthcare` expense category models only out-of-pocket costs so the premium is not double-counted.
- FR-19: **Healthcare funding scheme is always shown** — every tab displays a badge for the selected
  city/country derived from `Country.healthcareModelType` (e.g. "Healthcare: tax-funded (NHS-style)",
  "mandatory payroll insurance", or "out-of-pocket"), **with the full badge label fully visible (not
  clipped) inside its row**. The `healthcare` expense category models out-of-pocket costs **only**; for
  `tax-funded`/`mixed` countries it is the small residual (prescriptions, dental, copays, optical) since
  mandatory premiums sit inside the effective tax rate. The "OOP = out-of-pocket" abbreviation in the
  Healthcare (OOP) column header is explained on screen per **FR-22**.
- FR-20: Kids split by stage — **pre-school-age children incur childcare** (per pre-school child,
  an essential) and **school-age children incur schooling** (per school-age child). The shared kids
  control is two number inputs (pre-school 0–3, school-age 0–3); every city carries
  `childcareMedianLocal` and a `{ public, private }` school median.
- FR-21: The Savings and Minimum-role tabs report **two** savings figures — `essentialSavings`
  (`net − essentials`) and `afterLifestyleSavings` (`essentialSavings − lifestyle`) — each shown in
  local + USD. The Minimum-role tab **ranks on `essentialSavings`**; lifestyle is excluded from the
  ranking.
- FR-22: **On-screen "OOP = out-of-pocket" explanation** — every tab that shows the **Healthcare (OOP)**
  column displays an on-screen explanation (a legend/footnote line, e.g. "OOP = out-of-pocket —
  healthcare you pay yourself, on top of any tax-funded or insurance coverage") so the abbreviation in
  the column header is never unexplained. The explanation is localized (en/id) and is repeated in the
  city-detail healthcare panel.
- FR-23: **Shared cost-basis controls on all three tabs (including Minimum role)** — the **household**
  (adults + pre-school-kid count + school-age-kid count), **area** (center / rural), and **school-type**
  (public / private) controls, together with the **Region / Country / City** geographic filters, form a
  single shared control set present and applied on **every tab, including Minimum role**. The
  Minimum-role essential-savings computation (and therefore which role is the minimum) uses the active
  household / area / school basis, because a role's essential savings falls as the modeled essentials
  rise with household size, central area, and private schooling.

## Non-Functional Requirements

- NFR-1: **Client-side rendered (CSR)** — a `'use client'` page; all inputs and computation happen in
  the browser. No server-side rendering of results, no backend/tRPC procedure, no runtime network.
- NFR-1b: Dataset lists **as many tech-hub cities worldwide as we reasonably can** (static), excl.
  Israel; breadth over a fixed small set. **ASEAN, Japan, broader Europe, and the Nordics must each
  be represented**, alongside the Americas, Middle East, South/East Asia, Oceania, and Africa.
- NFR-1c: The role-salary matrix (`roles.ts`) is static, `web-researcher`-sourced, and covers
  every role on the canonical ladder for every **country** referenced by `cities.ts` — no holes (each
  cell a `{ p25, median, p75 }` distribution + a non-salary-comp figure; gaps filled with documented
  `proxy` estimates, never fabricated exact figures) — with per-cell confidence tiers and a salary
  snapshot date. Cities inherit their country's distribution.
- NFR-1d: The per-country tax model (`countries`/tax bands) covers every country present in
  `cities.ts` — no city without a country tax band — each band confidence-tiered and snapshot-dated.
- NFR-1e: **Universal dual-currency display** — every monetary value rendered anywhere in the tool is
  formatted in **both** the city's local currency **and** USD, on every tab; no money figure is ever
  shown in only one currency. This explicitly includes the Minimum-role tab's **salary percentile
  columns (p25 / median / p75)** and **compensation columns (non-salary comp, total comp)**, not only
  the savings figure — each is dual. The minimum-role tab layers its user-chosen display currency on top
  (the display-currency selector chooses which currency occupies the primary line alongside local).
- NFR-2: WCAG AA — labeled inputs, keyboard-operable, sufficient contrast; responsive (mobile→desktop).
- NFR-2b: **Healthcare funding-scheme badge accessibility** — the always-shown healthcare-scheme badge
  conveys its meaning by **text label**, not colour alone; it is keyboard-focusable/announced and meets
  AA contrast so screen-reader and colour-blind users get the scheme (tax-funded / mandatory payroll
  insurance / out-of-pocket) unambiguously on every tab.
- NFR-3: Calculation core is pure and unit-tested; components have tests; the companion Gherkin feature
  (`specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/cost-of-living-calculator.feature`) is
  consumed by both the **unit** tier (`@amiceli/vitest-cucumber`, external deps mocked, which satisfies
  `specs:coverage`) and the fe-e2e tier (`playwright-bdd`/`bddgen`) — no hand-written e2e spec
  duplicates the scenarios. ayokoding-www has **no integration tier** (`test:integration` is a no-op
  `echo`; integration is reserved for app-tier products such as `organiclever-app-web`).
- NFR-4: No new runtime dependencies beyond those `ayokoding-www` already ships.

## Disclaimers

The tool shows a visible **Disclaimers** block (localized en/id) covering:

- Savings are computed **before** any voluntary pension/retirement contributions.
- **Clothing and personal care are folded into "lifestyle"**, not separate categories.
- **Nominal FX vs PPP** — a positive USD savings figure does **not** mean equal purchasing power; USD
  uses a **nominal FX snapshot**, not a PPP (real purchasing-power) conversion.
- Data and FX are a **snapshot** and may be stale; figures are **single-point median estimates**;
  smaller-city figures are less reliable (may be proxy or older).
- **Tax is simplified** — a banded effective rate (federal + sub-national for US/CA/CH only); it
  excludes filing status, deductions, benefits-in-kind, and social-contribution caps.
- **Healthcare** models **out-of-pocket costs only**; the funding scheme (tax-funded / mandatory
  payroll insurance / out-of-pocket) is shown per country so the user knows what is and isn't included.
- **Relocation** sunk costs (deposit, key money, moving, visa/admin) are a one-time estimate kept out
  of the monthly savings math; the **cash cushion is a liquidity reserve the user keeps**, not a sunk
  cost.
- **Role salary is modeled at the national level** — each role's salary is a per-role × **country**
  `{ p25, median, p75 }` distribution and **cities inherit their country's figures**; salary is **not**
  city-specific, so a city's modeled role savings may be optimistic or pessimistic versus reality.
- **Non-salary comp (RSU/equity + bonus)** is shown only as **informational total-comp context** and
  is **not** part of the net-savings math — both savings figures use net **base salary only**. This is
  deliberate: RSU/equity value is **volatile** (it rises and falls with the share price, and bonuses
  are not guaranteed), so including it would make savings unstable; equity vesting and equity tax are
  also not modeled.

## Product Risks

| Risk                                                                                                                                              | Impact | Mitigation                                                                                                                                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Data freshness perception** — static snapshot data may look stale if months pass without a refresh                                              | Med    | `fxSnapshotDate` + per-cell confidence tier + "estimates only" disclaimer communicates the trade-off; dataset curation is a low-frequency task                                  |
| **Over-reliance on estimates for financial decisions** — users may treat modeled figures as precise enough to base a relocation or negotiation on | Med    | Prominent "estimates only" disclaimer + confidence flags on low-confidence cells; PRD scope explicitly excludes live/precise data; disclaimer in both locales                   |
| **Scope expansion** — pressure to add more tabs (PPP comparison, charts, live FX, bracket engine) post-launch                                     | Med    | Explicit Out of Scope list locks v1; additional tabs deferred to later iterations; plan references this scope boundary                                                          |
| **EN + ID audience only** — visitors from other language backgrounds receive no localized experience                                              | Low    | v1 explicitly scopes EN + ID; adding more locales is a future plan item; tool is still fully readable in English                                                                |
| **i18n coverage gap** — a translation key added in code but missing from `translations.ts` silently falls back to the key string                  | Low    | Phase 3 delivery step validates all calculator UI strings present in both locale branches; `typecheck` + `lint` catch missing keys at build time                                |
| **Tool misused as a financial advisor** — a visitor acts on the output without understanding the model's simplifications                          | Med    | Disclaimers block covers each simplification explicitly (simplified tax, national-level salary, estimates-only, nominal FX not PPP); no budgeting-advice framing in any UI copy |
| **Role ladder misread as a generic salary ladder** — visitor does not notice the "software-engineering roles (IC + management)" caption           | Low    | Caption is a mandatory UI element (FR enforced by component test + Gherkin scenario); labeled in both locales                                                                   |

## Out of Scope

Live cost-of-living / FX / **salary** / **tax** APIs (all datasets are static for v1);
**full progressive tax-bracket engines**; **social-contribution caps**; **benefits-in-kind**;
**pension / retirement contribution modeling**; **clothing / personal-care as separate categories**;
**PPP-adjusted (real purchasing-power) comparison**; **per-individual tax situations** (filing status,
dependents-as-tax-credits, local surtaxes beyond the modeled US/CA/CH sub-national rate);
**equity / RSU / bonus modeling into savings** (the typical non-salary comp is **displayed** as
informational total-comp context, but equity vesting/tax is never folded into the deterministic
net-savings math); **deduction optimization**; **per-city (sub-national) role-salary granularity**
(salary is modeled per role × country and cities inherit it); savings goals; persistence / share /
export; per-city non-default currencies; per-city household/area-cost overrides (v1 uses shared
multiplier tables); school-cost granularity beyond a city public/private median; per-person
career-progression modeling; charts; and any Israeli city. These are candidates for later iterations.
