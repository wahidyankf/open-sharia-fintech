# Product Requirements — Vercel Function Cost Reduction

## Product overview

This is a performance-and-cost change with a **strict no-visible-regression requirement**. Every
page, URL, redirect, language variant, and interactive behaviour that works today must work
identically afterwards. The only user-visible difference should be that pages load faster.

The work converts server-rendered-per-request pages into build-time-prerendered pages served from
the CDN. Two behaviours currently computed on the server move to the client, so the product
requirement is that they remain functionally equivalent from the reader's point of view.

## Personas

| Persona                    | Need                                                                                        |
| -------------------------- | ------------------------------------------------------------------------------------------- |
| Content reader (ayokoding) | Reads courses and lessons in English or Indonesian; follows deep links and bookmarks        |
| Course-path follower       | Navigates within a learning path via `?path=` context and expects the sidebar to reflect it |
| CV/portfolio visitor       | Lands on wahidyankf.com, filters content with a search box, may share a filtered URL        |
| Search engine crawler      | Must reach, render, and index every public page                                             |
| Site owner                 | Budgets $30, backstops at $35, wants it at the $20 subscription                             |

## User stories

- As a **content reader**, I open a course lesson URL and see the same page I see today, faster, with
  the correct `<html lang>` for my locale.
- As a **content reader**, I visit `/` and am still redirected to `/en`.
- As a **content reader** who typed an uppercase locale (`/EN/...`), I am still redirected to the
  lowercase canonical URL.
- As a **course-path follower**, I open a lesson with `?path=<id>` and the sidebar still shows my
  path context, with prerequisite links resolving as they do today.
- As a **CV visitor**, I open `/cv?search=rust` and the page still opens with the search box
  pre-filled and results filtered.
- As a **crawler**, I can fetch `robots.txt` and `sitemap.xml` from wahidyankf.com (neither exists
  today) and I remain able to crawl and index every public page on both sites.
- As the **site owner**, I can see a configured spend cap that will pause production deployments
  before my bill runs away, set at $35 rather than at my $30 budget so it fires only on a genuine
  runaway — and I understand that pausing takes the sites down until I resume each project by hand.

## Behaviour that must not regress

These are the specific behaviours whose implementation moves, and which therefore carry the highest
regression risk. Each has a Gherkin scenario below.

| Behaviour                         | Today                                                       | After                                                                             |
| --------------------------------- | ----------------------------------------------------------- | --------------------------------------------------------------------------------- |
| `<html lang>` reflects the locale | Root layout reads middleware's `x-pathname` via `headers()` | `app/[locale]/layout.tsx` (promoted to root layout) reads `params.locale`         |
| `?path=` course-path context      | Read server-side in the `[...slug]` page                    | Read client-side via `useSearchParams()` — already the case in `sidebar-host.tsx` |
| `/` → `/en` redirect              | Middleware                                                  | `next.config.ts` `redirects()`, evaluated at the edge routing layer               |
| Uppercase-locale normalisation    | Middleware 308                                              | `next.config.ts` `redirects()`, enumerated per locale variant                     |
| `?search=` on wahidyankf routes   | Read server-side via `searchParams`                         | Read client-side via `useSearchParams()` inside `<Suspense>`                      |
| All 74 existing redirect rules    | `next.config.ts` `redirects()`                              | Unchanged — explicitly not touched                                                |

## Product scope

**In scope — user-facing surface**

- `apps/ayokoding-www`: all `[locale]` routes and the `(content)/[...slug]` catch-all.
- `apps/wahidyankf-www`: `/`, `/cv`, `/personal-projects`, plus new `robots.ts` and `sitemap.ts`.
- `apps/organiclever-app-web`: `/system/status/be` becomes non-indexable.

**Out of scope — user-facing surface**

- No content is added, removed, reworded, or re-slugged.
- No visual, layout, styling, or copy changes on any page.
- No change to the search dialog, the mobile navigation drawer, the tools pages, or the
  `ModelTable`/chart surfaces owned by the sibling AI-benchmark plan.
- No change to `ose-www`, `organiclever-www`, `ose-app-web`, or the web-ui Storybook UI.

## Acceptance criteria (Gherkin)

```gherkin
Feature: Content pages are statically prerendered and CDN-cached

  Background:
    Given the ayokoding-www site is built and deployed

  Scenario: A content page is prerendered at build time
    When the build output manifest is inspected
    Then the prerendered route count is at least two thousand
    And the content catch-all route is not marked as dynamically rendered

  Scenario: A repeat request to a content page is served from the CDN
    Given a visitor has already requested a course lesson URL
    When the same URL is requested again
    Then the response is served from the CDN cache
    And the response does not carry a no-store cache directive

  Scenario: The document language still reflects the locale
    When a visitor requests an English content page
    Then the html element declares the English language code
    When a visitor requests an Indonesian content page
    Then the html element declares the Indonesian language code
```

```gherkin
Feature: Course-path context survives the move to client-side resolution

  Scenario: A lesson opened with a path context shows that context
    Given a course path manifest exists
    When a visitor opens a lesson URL carrying a path query parameter
    Then the sidebar reflects the active path context
    And every resolvable prerequisite link is rendered

  Scenario: A lesson opened without a path context renders normally
    When a visitor opens a lesson URL with no path query parameter
    Then the lesson renders with no path context and no error
```

```gherkin
Feature: Locale entry redirects are preserved without middleware

  Scenario: The bare root redirects to the default locale
    When a raw HTTP GET is made to "/" with redirects disabled
    Then the response is a redirect
    And the response Location header points at the default locale root

  Scenario Outline: An uppercase locale prefix normalises to lowercase
    When a raw HTTP GET is made to "<legacy_url>" with redirects disabled
    Then the response status should be 308
    And the response Location header should equal "<canonical_url>"

    Examples:
      | legacy_url | canonical_url |
      | /EN        | /en           |
      | /ID        | /id           |
```

```gherkin
Feature: Search-filtered portfolio routes are static yet still filterable

  Background:
    Given the wahidyankf-www site is built and deployed

  Scenario: The three portfolio routes are statically prerendered
    When the build route table is inspected
    Then the home, cv, and personal-projects routes are all marked static
    And none of them is marked as dynamically rendered

  Scenario: A shared filtered URL still opens filtered
    When a visitor opens the cv route with a search query parameter
    Then the search input is pre-filled with that query
    And the visible entries are filtered to match it

  Scenario: The site exposes crawler directives
    When a crawler requests the robots file
    Then it resolves successfully and names the sitemap
    When a crawler requests the sitemap
    Then it resolves successfully and lists every public route
```

```gherkin
Feature: The billing outcome is verified, not assumed

  Scenario: Gross metered usage stays inside the budget goal
    Given a full billing cycle has elapsed at the new steady state
    When the cycle's infrastructure subtotal is read from the usage dashboard
    Then the gross metered usage is at or below thirty US dollars
    And the invoice total is at or below thirty US dollars

  Scenario: The backstop never had to fire
    Given a full billing cycle has elapsed at the new steady state
    When the spend management activity log is read for that cycle
    Then no project was paused
    And the invoice total is below thirty-five US dollars

  Scenario: Gross metered usage fits inside the included credit
    Given a full billing cycle has elapsed at the new steady state
    When the cycle's infrastructure subtotal is read from the usage dashboard
    Then the gross metered usage is below twenty US dollars
    And the on-demand charge above the subscription is zero

  Scenario: A spend cap exists as a backstop
    When the team billing settings are inspected
    Then a spend amount of fifteen US dollars is configured
    And the automatic pause action is enabled

  Scenario: The spend amount is understood as post-credit
    Given a spend amount of fifteen US dollars is configured
    When the amount that would trigger the pause is reasoned about
    Then it means fifteen US dollars of charge beyond the included credit
    And it implies a worst-case invoice of thirty-five US dollars
    And it does not mean fifteen US dollars of gross metered usage
```

These scenarios are deliberately separate: the **budget goal** ($30) is advisory and missing it is a
shortfall; the **backstop** ($35) is machine-enforced and firing it is an incident; the **target**
($20) is where the engineering is aimed. Collapsing them would lose the distinction the budget rests
on — see [tech-docs.md DD-9](./tech-docs.md#dd-9--15-spend-cap-as-a-soft-backstop-under-a-30-budget-goal).

```gherkin
Feature: The backend health-check page is excluded from search indexes

  Scenario: A crawler that does not execute JavaScript still sees the directive
    Given the backend health-check status page is deployed
    When a crawler requests that page and reads only the server-rendered HTML
    Then the response carries a robots directive marking the page as not indexable

  Scenario: The page remains reachable for humans
    When a person opens the backend health-check status page
    Then the page renders its health result as before
    And it is not redirected or blocked
```
