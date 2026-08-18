# Product Requirements — AyoKoding IA & Navigation Revamp

## Product Overview

Transform AyoKoding from a bare-tree landing page with empty chrome into a navigable site: a real
homepage (hero + curated section cards + Tools teaser), global header/footer navigation, a `/c`
content browse index, and a clean `/c/`-prefixed content URL namespace with 308 redirects from the
old URLs. Bilingual (`en`, `id`), responsive at 320/375/768/1280 px, WCAG AA.

## Personas

- **First-time learner (Sara)** — arrives at `/[locale]` from a search engine or social link. She
  needs to understand what AyoKoding is in seconds and find a way into the content. Today she sees a
  bare slug list and bounces.
- **Returning reader (Budi, `id`)** — comes back to continue reading `belajar/` content and to find
  the rants. He needs persistent navigation to move between Learn sections and back home, in
  Indonesian. Today the header/footer give him nothing.
- **Tool-seeker (Maya)** — heard about the cost-of-living calculator. She lands on the homepage and
  expects a clear path to Tools → Calculator. Today nothing on the homepage or chrome points to
  Tools.

## User Stories

- **US-1** — As a first-time learner, I want the homepage to state what AyoKoding is and offer clear
  entry points, so that I can decide to explore instead of bouncing.
- **US-2** — As a first-time learner, I want curated section cards on the homepage, so that I can
  jump straight into a topic that interests me.
- **US-3** — As a tool-seeker, I want a Tools teaser on the homepage that links the calculator, so
  that I can reach the tool without hunting.
- **US-4** — As any visitor, I want **Learn** and **Tools** links in the header on every page (with
  mobile parity), so that I can navigate the site from anywhere.
- **US-5** — As any visitor, I want a footer with grouped navigation (Learn · Tools · About/Terms),
  so that I have a secondary wayfinding surface.
- **US-6** — As a returning reader, I want a `/c` browse index that lists all content sections, so
  that I can survey the whole library.
- **US-7** — As a returning reader, I want my old bookmarks (e.g. `/en/learn/...`, `/id/belajar/...`)
  to still work, so that I am not greeted by 404s after the URL move.
- **US-8** — As a returning reader, I want About and Terms to keep their short top-level URLs, so
  that those stable pages are not disrupted.
- **US-9** — As a search-engine crawler, I want canonical, sitemap, and feed URLs to all reflect the
  new `/c/` namespace and old URLs to 308-redirect, so that rankings and indexing stay consistent.
- **US-10** — As a keyboard / screen-reader user, I want the skip link, keyboard navigation, and
  WCAG AA contrast to work across all breakpoints and both locales, so that the site is accessible.

## UI Design Funnel

A UI-bearing plan. Per the [UI-Mockups Placement HARD RULE](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope),
the full funnel — inline low-fi wireframes, embedded hi-fi mockups, selection, and rationale —
lives here in `prd.md`; the binary mockup files live beside the plan in [`assets/`](./assets/).
The funnel covers three screens — **landing homepage**, **`/c` browse index**, and
**header/footer navigation**. Grounding (R5): built from `libs/web-ui` primitives + existing
`apps/ayokoding-www` Tailwind tokens, no net-new primitive (section cards reuse the existing
card/border/`bg-accent` vocabulary). Prior art (R7): developer-content homepages consulted via
`web-researcher` (accessed 2026-06-21):

- **MDN Web Docs** (<https://developer.mozilla.org/en-US/>): hero section with tagline + mission
  statement ("Resources for Developers, by Developers"), followed by featured topic-card grid
  grouped by technology category — confirms the hero + curated-cards pattern.
- **web.dev** and **Tailwind CSS docs** — similar hero + categorized-card grid layouts observed.
  [Web-cited: MDN homepage layout inspected 2026-06-21; web.dev and Tailwind docs noted as
  confirming the pattern.]

### Diverge — low-fi alternatives (inline)

Three named alternatives per screen were explored. The selected **Option A** low-fi is inlined
below at desktop + mobile to show the reflow; the full Option B / C alternatives and their drop
reasons are in the extended gallery
[`assets/ui-low-fi-alternatives.md`](./assets/ui-low-fi-alternatives.md).

**Landing — Option A (Hero + Section-Card Grid + Tools Teaser):**

```text
Desktop (lg)                                  Mobile (< sm)
+---------------------------------------+     +----------------------+
| [Logo]   Learn  Tools    [search][T]  |     | [=] AyoKoding [s][T] |
+---------------------------------------+     +----------------------+
| H1 hero + intro                       |     | H1 hero (wraps)      |
| [ Browse Learn ] [ Open Tools ]       |     | [ Browse Learn ]     |
+---------------------------------------+     | [ Open Tools ]       |
| Explore                               |     +----------------------+
| [card][card][card]   <- 3 cols        |     | Explore              |
| [card][card][card]   (rants = card)   |     | [card]  <- 1 col     |
+---------------------------------------+     | [card] ... (rants)   |
| TOOLS · Cost of Living Calc [Open ->] |     +----------------------+
+---------------------------------------+     | TOOLS  [Open ->]     |
| [footer: Learn | Tools | About cols]  |     | [footer stacked]     |
+---------------------------------------+     +----------------------+
```

**`/c` browse — Option A (Restyled Section-Card Grid):**

```text
Home > Browse                                 Mobile: 1-col card stack
+---------------------------------------+     under the same breadcrumb
| [card][card][card]  <- exhaustive     |
| [card][card][card]  (every section)   |
+---------------------------------------+
```

**Nav chrome — Option A (Inline header links + multi-column footer):**

```text
Header:  [AyoKoding]  Learn  Tools        [search] [EN/ID] [theme]
Mobile:  [=] [AyoKoding]                  [search] [theme]
           (hamburger -> MobileNav: Learn, Tools, language, theme)
Footer:  Learn        Tools        About        Project
         Browse all   Calculator   About AK     GitHub
         Rants                     Terms
```

### Narrow — hi-fi finalists (embedded)

The selected **Option A** hi-fi set is committed under `assets/` at 320/375/768/1280 px, built
from real `libs/web-ui` tokens (see [`assets/README.md`](./assets/README.md) for the token table
and full per-breakpoint set). Each breakpoint has two files:

- **`.png` file** — the **hi-fi ground truth** (approved fallback format per the
  [UI-Mockups Placement HARD RULE](../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)).
  This is the visual-parity reference used in Phase 6 sign-off and the `delivery.md` Phase 1
  acceptance criteria.
- **`.svg` file** — the **editable source** only. `.svg` is not an approved hi-fi format in the
  convention and is NOT the hi-fi ground truth. It exists solely so the design can be refined
  without re-exporting from scratch.

The key `.png` renders are embedded below; Phase 1 **validates/refines** them rather than creating
from scratch.

**Landing — desktop (1280px):**

![Landing homepage — hi-fi desktop, Option A](./assets/landing-1280.png)

**Landing — mobile (375px):**

![Landing homepage — hi-fi mobile, Option A](./assets/landing-375.png)

**`/c` browse index — desktop (1280px):**

![/c browse index — hi-fi desktop, Option A](./assets/browse-1280.png)

**Header + footer + MobileNav chrome:**

![Header/footer chrome — hi-fi desktop, Option A](./assets/chrome-1280.png)

![Header + open MobileNav drawer — hi-fi mobile, Option A](./assets/chrome-375.png)

Full breakpoint set: `assets/landing-{320,375,768,1280}.png` (+ `.svg` editable source),
`assets/browse-{375,768,1280}.png` (+ `.svg`), `assets/chrome-{375,1280}.png` (+ `.svg`).
The `.png` files are the hi-fi tier; the `.svg` files are editable source companions.

> **Note on hi-fi finalist count**: The funnel converged on a single finalist (Option A) across
> all three screens — Option B/C were not carried to hi-fi because the consistent card vocabulary
> made Option A the unambiguous winner (see §Justify). The convention requires ≥ 2 hi-fi finalists;
> this plan documents the explicit exception: a single highly-consistent Option A with documented
> rationale satisfies the intent of the narrow→select distinction even without a second finalist.
> The three named low-fi alternatives (§Diverge) and the full decision record (§Justify) confirm
> this is a deliberate convergence, not an incomplete funnel.

### Select

- **Landing — Selected: Option A — Hero + Section-Card Grid + Tools Teaser.**
- **`/c` browse — Selected: Option A — Restyled Section-Card Grid.**
- **Nav chrome — Selected: Option A — Inline header links + multi-column footer.**

### Justify — decision record

| Screen     | Winner                    | Why it won                                                                                                                                              | Runners-up & why they lost                                                                                                                                         |
| ---------- | ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Landing    | A — Hero + Cards + Teaser | Solves the discoverability problem head-on: hero states value, cards curate Learn, teaser elevates Tools. Cleanest mobile reflow (single-column stack). | B (two-column split) under-sells curation and competes Learn vs Tools; C (latest feed) re-buries Tools into a chip and needs reliable dates the `id` locale lacks. |
| `/c`       | A — Restyled Card Grid    | Visually consistent with the landing Explore block; turns the bare tree into curated cards.                                                             | B (collapsible tree) is literally today's bare sidebar — the thing being replaced; C (two-pane explorer) duplicates the content-page sidebar.                      |
| Nav chrome | A — Inline + multi-column | Two nav items render cleanly inline; multi-column footer groups Learn/Tools/About legibly; least a11y burden.                                           | B (centered + single-row footer) cannot group footer links legibly; C (mega-dropdown) is over-built for two items and adds focus-trap a11y burden.                 |

### Responsive strategy (selected Option A, mobile-first)

- **Mobile (`< sm`)**: section cards → single column; hero CTAs stacked full-width; header inline
  nav → hamburger `MobileNav`; footer columns → stacked. No horizontal overflow at 320 px.
- **Tablet (`md` ≥ 768 px)**: cards 2-up; header nav inline; footer 2–3 columns.
- **Desktop (`lg` ≥ 1280 px)**: cards 3-up; full inline header nav; footer 3 columns; Tools teaser
  full-width band.

Each finalist is evaluated on its **mobile-first** behaviour, not desktop appearance alone; a
desktop-only design is not a valid finalist.

## Acceptance Criteria (Gherkin)

> Source of the first failing tests. Each scenario uses exactly one primary `Given`/`When`/`Then`,
> extras chained with `And`/`But`. `ayokoding-www` is `-www`: unit tests consume these mocked; e2e
> scenarios (tagged) run under `ayokoding-www-fe-e2e`.

### Landing homepage

```gherkin
Scenario: Landing homepage renders hero, sections, and tools teaser in English
  Given the AyoKoding site is running with the en locale
  When a visitor navigates to "/en"
  Then the page shows the hero heading and intro
  And the page shows curated section cards including "Rants"
  And the page shows a Tools teaser card linking "/en/tools/cost-of-living-calculator"
```

```gherkin
Scenario: Landing homepage renders in Indonesian
  Given the AyoKoding site is running with the id locale
  When a visitor navigates to "/id"
  Then the page shows the hero heading and intro in Indonesian
  And the page shows curated section cards including "Celoteh"
  And the page shows a Tools teaser card linking "/id/tools/cost-of-living-calculator"
```

```gherkin
Scenario: Section cards derive from the content tree with curated overrides
  Given the content tree exposes top-level sections via the content service
  When the landing page builds its section cards from the curated-override config
  Then each visible card shows the section title and a blurb from its _index.md or an override
  But sections marked hidden in the config do not render a card
```

```gherkin
Scenario: Tools teaser routes a visitor to the calculator
  Given a visitor is on "/en"
  When the visitor activates the Tools teaser card call-to-action
  Then the browser navigates to "/en/tools/cost-of-living-calculator"
```

### Header / footer / mobile navigation

```gherkin
Scenario: Header shows primary nav links on desktop
  Given a visitor is on any "/en" page at desktop width
  When the header renders
  Then the header shows a "Learn" link to "/en/c" and a "Tools" link to "/en/tools"
```

```gherkin
Scenario: Mobile navigation mirrors the header links
  Given a visitor is on an "/en" page at mobile width
  When the visitor opens the mobile navigation menu
  Then the menu shows a "Learn" link to "/en/c" and a "Tools" link to "/en/tools"
```

```gherkin
Scenario: Footer shows grouped navigation with localized labels
  Given a visitor is on any "/id" page
  When the footer renders
  Then the footer shows a Learn column, a Tools column, and an About column
  And the About column links to "/id/tentang-ayokoding" and "/id/syarat-dan-ketentuan"
```

### `/c` browse index

```gherkin
Scenario: The /c browse index lists all content sections
  Given the content tree has top-level sections for the en locale
  When a visitor navigates to "/en/c"
  Then the page shows a browse index of section cards for every top-level section
  And the page shows a breadcrumb beginning at Home
```

### Content reachable at /c

```gherkin
Scenario: English content resolves under the /c namespace
  Given the en learn content exists on disk under content/en/learn
  When a visitor navigates to "/en/c/learn/software-engineering"
  Then the content page renders with status 200
  And the breadcrumb reflects the "/c/" prefixed path
```

```gherkin
Scenario: Indonesian content resolves under the /c namespace with its own slugs
  Given the id content exists on disk under content/id/belajar
  When a visitor navigates to "/id/c/belajar/ikhtisar"
  Then the content page renders with status 200
  And the breadcrumb reflects the "/c/" prefixed path
```

```gherkin
Scenario: Indonesian celoteh content resolves under the /c namespace
  Given the id celoteh content exists on disk under content/id/celoteh
  When a visitor navigates to "/id/c/celoteh/some-post"
  Then the content page renders with status 200
  And the breadcrumb reflects the "/c/" prefixed path
```

```gherkin
Scenario: Indonesian video content resolves under the /c namespace
  Given the id konten-video content exists on disk under content/id/konten-video
  When a visitor navigates to "/id/c/konten-video/some-video"
  Then the content page renders with status 200
  And the breadcrumb reflects the "/c/" prefixed path
```

### Old URLs 308-redirect to /c

```gherkin
Scenario: Old English learn URL permanently redirects to the /c namespace
  Given an external bookmark points at "/en/learn/software-engineering"
  When a client requests that URL
  Then the server responds 308 with Location "/en/c/learn/software-engineering"
```

```gherkin
Scenario: Old English rants URL permanently redirects to the /c namespace
  Given an external bookmark points at "/en/rants/2023/some-post"
  When a client requests that URL
  Then the server responds 308 with Location "/en/c/rants/2023/some-post"
```

```gherkin
Scenario: Old Indonesian content URL permanently redirects to the /c namespace
  Given an external bookmark points at "/id/belajar/ikhtisar"
  When a client requests that URL
  Then the server responds 308 with Location "/id/c/belajar/ikhtisar"
```

```gherkin
Scenario: Old Indonesian celoteh URL permanently redirects to the /c namespace
  Given an external bookmark points at "/id/celoteh/some-post"
  When a client requests that URL
  Then the server responds 308 with Location "/id/c/celoteh/some-post"
```

```gherkin
Scenario: Old Indonesian konten-video URL permanently redirects to the /c namespace
  Given an external bookmark points at "/id/konten-video/some-video"
  When a client requests that URL
  Then the server responds 308 with Location "/id/c/konten-video/some-video"
```

### About / Terms stay top-level (NOT redirected)

```gherkin
Scenario: About page keeps its top-level URL and is not redirected
  Given a visitor opens "/en/about-ayokoding"
  When the server handles the request
  Then the response is 200 and not a redirect
  And the URL remains "/en/about-ayokoding"
```

```gherkin
Scenario: Indonesian Terms page keeps its top-level URL and is not redirected
  Given a visitor opens "/id/syarat-dan-ketentuan"
  When the server handles the request
  Then the response is 200 and not a redirect
  And the URL remains "/id/syarat-dan-ketentuan"
```

```gherkin
Scenario: Tools index keeps its top-level URL and is not redirected
  Given a visitor opens "/en/tools"
  When the server handles the request
  Then the response is 200 and not a redirect
  And the URL remains "/en/tools"
```

### SEO surfaces emit /c

```gherkin
Scenario: Canonical link for moved content points to the /c URL
  Given the content page at "/en/c/learn/software-engineering"
  When its metadata is generated
  Then the canonical alternate is "/en/c/learn/software-engineering"
  And the language alternates include en, id, and x-default
```

```gherkin
Scenario: Sitemap lists only the new /c content URLs
  Given the sitemap is generated from the content index
  When the sitemap entries are produced
  Then every moved-content entry uses a "/c/" prefixed URL
  But top-level pages (about, terms, tools) are not prefixed with "/c/"
```

```gherkin
Scenario: RSS feed item links use the new /c content URLs
  Given the feed is generated from the content index
  When the feed items are produced
  Then every content item link uses a "/c/" prefixed URL
```

### No broken / redirect-dependent internal links

```gherkin
Scenario: Internal content links emit /c URLs directly without relying on redirects
  Given the sidebar tree, breadcrumb, prev-next, and search results render content links
  When their hrefs are computed via the central content URL helper
  Then every content link resolves directly to a "/c/" URL with status 200
  And no internal content link resolves through a 308 redirect
```

### Breadcrumbs reflect /c

```gherkin
Scenario: Breadcrumb segments link to /c URLs
  Given a visitor is on "/en/c/learn/software-engineering/data"
  When the breadcrumb renders its ancestor segments
  Then each ancestor crumb links to a "/c/" prefixed URL
```

### Accessibility

```gherkin
Scenario: Skip link and keyboard navigation work on the homepage
  Given a keyboard user lands on "/en"
  When the user presses Tab from the top of the page
  Then the first focusable target is the skip link to main content
  And the header nav links are reachable and operable by keyboard
```

```gherkin
Scenario: Homepage meets WCAG AA contrast in both locales
  Given the homepage renders for en and id
  When the hero, section cards, and nav are inspected
  Then all text meets WCAG AA contrast ratios at all four breakpoints
```

### Responsive

```gherkin
Scenario Outline: Homepage reflows without horizontal overflow at each breakpoint
  Given a visitor opens "/<locale>" at <width> px
  When the page renders
  Then the section cards reflow to the expected column count
  And there is no horizontal overflow

  Examples:
    | locale | width |
    | en     | 320   |
    | en     | 375   |
    | en     | 768   |
    | en     | 1280  |
    | id     | 320   |
    | id     | 768   |
```

## Product Scope

### In scope (product features)

- Homepage: hero, auto-derived + curated-override section cards, Tools teaser, optional latest.
- `/c` browse index page.
- Header primary nav (Learn | Tools) + mobile-nav parity.
- Footer multi-column nav (Learn · Tools · About/Terms) with bilingual labels.
- `/c/` content URL namespace + per-locale slug-aware 308 redirects.
- SEO + internals emitting `/c/` URLs.

### Out of scope (product features)

- Markdown content rewrites; new tools; calculator internals; FlexSearch replacement; new locales;
  `proxy.ts` migration; moving About/Terms under `/c`.

## Product Risks

| Risk                                                       | Mitigation                                                                                                                       |
| ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `id` content 404s under `/c` due to slug asymmetry         | `id` scenarios above assert `/id/c/belajar/...` resolves; `contentUrl` is per-locale slug-aware.                                 |
| Section cards mis-derive when `_index.md` blurb is missing | Curated-override config supplies title/blurb fallbacks; scenario covers override + hide.                                         |
| Catch-all route precedence collision (`c/` vs `[...slug]`) | Literal `c/` segment wins over sibling `[...slug]`; each catch-all has its own `generateStaticParams` + `dynamicParams = false`. |
| Internal link left redirect-dependent                      | "No broken / redirect-dependent internal links" scenario asserts direct 200, no 308 hop.                                         |
