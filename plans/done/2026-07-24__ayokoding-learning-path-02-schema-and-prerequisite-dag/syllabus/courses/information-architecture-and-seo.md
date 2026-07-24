# Information Architecture and SEO (Annotated-concept, HTML)

**Course ID**: `information-architecture-and-seo` · **Format**: Annotated-concept · **Language**: HTML.

**Short summary**: Structuring content, optimizing for search

**Scope note**: making content findable and legible to both machines and people — taxonomy and URL
design, semantic HTML, sitemaps, structured data (schema.org), and Core Web Vitals as an SEO signal.
An annotated-concept topic: the deliverables are markup and structure, exercised against real
crawler/validation tooling rather than an application build. `‡ HTML †`: the worked artifacts are
semantic HTML and structured-data markup.

## Why this exists · the big idea

- **The problem before the solution**: content that humans can read is often invisible to machines —
  a beautiful page with `<div>` soup, opaque URLs, and no structured data can't be crawled, ranked,
  or understood by a search engine or assistive tech, so it doesn't get found. "Looks fine in a
  browser" is not the same as "legible to the systems that decide who sees it".
- **Keep-this-if-you-forget-everything**: structure _is_ meaning — a clear taxonomy, honest URLs,
  semantic HTML, and explicit structured data let machines and people navigate the same content, and
  findability follows from that shared structure, not from keyword tricks.
- **Big ideas touched**: `coupling-vs-cohesion` (a good information architecture groups what belongs
  together and separates what doesn't, so navigation and URLs stay stable as content grows),
  `layering-and-leaks` (the same page is read by a browser, a crawler, and a screen reader — semantic
  markup is the layer that serves all three, and where it's missing, each consumer's view diverges).

## Prerequisites

- **Prior topics**: [topic 14 Frontend Essentials](./frontend-essentials.md) (HTML semantics,
  accessibility, the document outline) and [topic 47 Advanced Frontend](./advanced-frontend.md)
  (rendering models — CSR/SSR/SSG — and their crawlability and performance consequences).
- **Tools & environment**: a macOS/Linux terminal; a browser with Lighthouse/DevTools; a structured-
  data validator (Schema.org / Rich Results test) and a Core Web Vitals measurement tool; the ability
  to serve static HTML locally; Neovim/VSCode with an HTML LSP (DD-17).
- **Assumed knowledge**: writing semantic HTML and understanding accessibility roles (topic 14); how
  server- vs client-rendering affects what a crawler sees (topic 47); serving files from the CLI
  (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: **Core Web Vitals** remain a Google ranking signal and the metric set is left
  correctly version-unpinned — the specific thresholds and the constituent metrics (notably the LCP/
  CLS pair and the interaction-responsiveness metric that replaced First Input Delay) shift over time,
  so measure with current tooling rather than hard-coding numbers.
- 2026-07-12 — verified: **schema.org** structured data (JSON-LD as the recommended embedding) and
  **sitemaps.org** XML sitemaps are stable, standard, and left unpinned. Validate against the current
  Rich Results / structured-data test at drafting time, as eligible rich-result types change.

> DD-35 primary-source pass (2026-07-12). Protocol limits, directive names, and thresholds traced to
> primary sources (RFC 9309, sitemaps.org, Google Search Central, ogp.me, W3C WAI, NN/g, MDN) and
> fetched/read. Char-length "rules" that vendors do NOT publish are called out. Unverifiable items flagged.

- **Information architecture** — the four systems (organization, labeling, navigation, search) trace to
  Rosenfeld, Morville & Arango, _Information Architecture: For the Web and Beyond_ (4th ed., O'Reilly, 2015,
  the "Polar Bear book"). Book body text was not directly fetchable (O'Reilly 403); metadata `[Verified]`,
  exact in-book definitions `[Needs Verification]`.
- **Card sorting / tree testing** — card sorting = "study participants place individually labeled cards into
  groups according to criteria that make the most sense to them" (open = no predefined categories, closed =
  all predefined); tree testing = "an evaluation of a hierarchical category structure … by having users find
  the locations … where specific resources … can be found." Card sorting is generative; tree testing
  evaluative. Sources: [NN/g Card Sorting](https://www.nngroup.com/articles/card-sorting-definition/), [NN/g Tree Testing](https://www.nngroup.com/articles/tree-testing/) (fetched, verbatim).
- **URL structure** — "use hyphens (`-`) instead of underscores (`_`) to separate words"; "use readable
  words rather than long ID numbers"; URLs are case-sensitive. Source: [Google — URL Structure Best Practices](https://developers.google.com/search/docs/crawling-indexing/url-structure) (fetched, verbatim).
- **Semantic HTML / headings** — "Do not skip heading levels: always start from `<h1>`, followed by `<h2>`
  and so on"; "A page should generally have a single `<h1>` … (similar to the document's `<title>`)"; `<nav>`
  has the implicit ARIA role `navigation`. Note a genuine nuance: **MDN** treats single-`<h1>` as best
  practice while **W3C WAI** is more permissive about multiple rank-1 headings — the firmer shared rule is
  don't skip ranks. Sources: [MDN Heading Elements](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/Heading_Elements), [W3C WAI Headings](https://www.w3.org/WAI/tutorials/page-structure/headings/) (fetched).
- **XML sitemaps** — "each Sitemap file … must have no more than **50,000 URLs** and must be no larger than
  **50MB (52,428,800 bytes)**"; namespace `http://www.sitemaps.org/schemas/sitemap/0.9`; a `<sitemapindex>`
  references child `<sitemap>` entries (also capped at 50,000 / 50MB). Source: [sitemaps.org protocol](https://www.sitemaps.org/protocol.html) (fetched, verbatim).
- **robots.txt (RFC 9309)** — "The rules MUST be accessible in a file named '/robots.txt' (all lowercase) in
  the top-level path"; "The parsing limit MUST be at least 500 kibibytes"; "Crawlers SHOULD NOT use the
  cached version for more than 24 hours"; if unreachable "the crawler MUST assume complete disallow."
  Directives: `user-agent`, `allow`, `disallow`. Source: [RFC 9309 (IETF, 2022)](https://www.rfc-editor.org/rfc/rfc9309.html) (fetched, verbatim).
- **Meta robots / X-Robots-Tag** — `<meta name="robots" content="noindex">` and `X-Robots-Tag: noindex`;
  valid values include `noindex`, `nofollow`, `none`, `nosnippet`, `max-snippet`, `noarchive` is
  **retired**. Source: [Google — Robots Meta Tags](https://developers.google.com/search/docs/crawling-indexing/robots-meta-tag) (fetched).
- **Canonical URLs** — "Canonicalization is the process of selecting the representative –canonical– URL"; the
  `rel="canonical"` indication is **"a hint, not a rule"** (Google may pick a different canonical). Source:
  [Google — Consolidate Duplicate URLs](https://developers.google.com/search/docs/crawling-indexing/canonicalization) (fetched, verbatim).
- **Crawling vs indexing** — crawl budget = "The set of URLs that Google can and wants to crawl" (crawl
  capacity + crawl demand); "Not every page that is crawled will necessarily be indexed"; explicitly a
  **large-site** concern (1M+ pages). Source: [Google — Managing Crawl Budget](https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget) (fetched).
- **Mobile-first indexing** — "Google uses the mobile version of a site's content, crawled with the
  smartphone agent, for indexing and ranking"; rollout completed/announced October 2023. Content, metadata,
  and structured data must match between mobile and desktop. Source: [Google — Mobile-First Indexing](https://developers.google.com/search/docs/crawling-indexing/mobile/mobile-sites-mobile-first-indexing) (fetched).
- **Titles / meta descriptions** — Google documents **no exact character limit**: snippets are "truncated …
  as needed, typically to fit the device width." The common "155–160 char" figure is folk knowledge, not a
  Google threshold. `<meta name="description">` may be overridden by an auto-generated snippet. Sources:
  [Google — Title Links](https://developers.google.com/search/docs/appearance/title-link), [Snippets](https://developers.google.com/search/docs/appearance/snippet) (fetched).
- **Structured data** — Google "recommend[s] … JSON-LD" (Microdata/RDFa also supported); schema.org is "a
  collection of shared vocabularies … understood by the major search engines," launched June 2, 2011 by
  Bing, Google, Yahoo!. Rich results = "search results that are more engaging." Sources: [Google — Structured Data Intro](https://developers.google.com/search/docs/appearance/structured-data/intro-structured-data), [schema.org getting started](https://schema.org/docs/gs.html) (fetched).
- **Open Graph** — "The four required properties for every page are: `og:title`, `og:type`, `og:image`,
  `og:url`." Source: [ogp.me](https://ogp.me/) (fetched, verbatim). Twitter/X Cards use `name`/`content`
  (`<meta name="twitter:card" content="summary">`, types `summary`/`summary_large_image`/`app`/`player`) —
  `[Needs Verification]` (developer.x.com returned HTTP 402; corroborated via search only).
- **hreflang** — `<link rel="alternate" hreflang="[lang]" href="…" />`; "Each language version must list
  itself as well as all other language versions"; URLs must be fully-qualified; `x-default` for unmatched
  locales. Source: [Google — Localized Versions](https://developers.google.com/search/docs/specialty/international/localized-versions) (fetched, verbatim).
- **Redirects** — 301 Moved Permanently ("Show the new redirect target in search results"); 302 Found /
  temporary ("Show the source page in search results"); 308 Permanent Redirect "has the same semantics as
  301 … [but] the user agent must not change the HTTP method." Sources: [MDN Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status), [Google — 301 Redirects](https://developers.google.com/search/docs/crawling-indexing/301-redirects) (fetched, verbatim).
- **Core Web Vitals as a signal** — LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1 (75th percentile); INP replaced
  FID in 2024. But "There is no single signal … page experience … [is] one input among many" — do not frame
  CWV as _the_ ranking factor. Sources: [web.dev — Core Web Vitals](https://web.dev/articles/vitals), [Google — Page Experience](https://developers.google.com/search/docs/appearance/page-experience) (fetched).
- **Internal linking / PageRank** — Brin & Page, "The Anatomy of a Large-Scale Hypertextual Web Search
  Engine," _Computer Networks and ISDN Systems_ 30(1–7), 1998, pp. 107–117: `PR(u) = Σ_{v∈Bu} PR(v)/L(v)`.
  Citation `[Verified]` (Stanford original timed out; formula corroborated via Wikipedia) — flag exact
  formula as `[Needs Verification]` if quoted verbatim.
- **Accessibility ↔ SEO** — WCAG 2.2 SC 1.1.1 (Level A): "All non-text content … has a text alternative
  that serves the equivalent purpose"; decorative images take `alt=""`. W3C publishes **no char limit** for
  alt text. Source: [W3C — Understanding 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html) (fetched, verbatim).
- **Measuring** — Google Search Console reports Index Coverage, Search Performance, Sitemaps, URL
  Inspection, Core Web Vitals; Lighthouse has an SEO audit category. The Lighthouse SEO doc page carried a
  stale 2019 timestamp — re-verify the current audit set against a live run. Sources: [Search Console overview](https://developers.google.com/search/docs/monitor-debug/search-console-start), [Lighthouse SEO](https://developer.chrome.com/docs/lighthouse/seo/) (fetched).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Annotated-concept). Each example below cites the co-NN it exercises. -->

- **co-01 · information-architecture** — IA is the organization, labeling, navigation, and search
  systems that make content findable and understandable (Rosenfeld/Morville/Arango four systems).
- **co-02 · findability-information-scent** — a label carries "scent" when it signals its destination;
  good IA matches how users actually look for things.
- **co-03 · card-sorting** — a generative method where participants group labeled cards by their own
  mental model (open = no fixed categories; closed = fixed categories) to discover a taxonomy.
- **co-04 · tree-testing** — an evaluative method that tests whether users can locate items in a
  proposed hierarchy, independent of visual design.
- **co-05 · taxonomy-hierarchy** — designing category structure and labels so related content groups
  together and navigation stays stable as content grows.
- **co-06 · url-structure** — readable, hierarchical URLs use hyphens (not underscores), words (not opaque
  IDs), and a stable path scheme.
- **co-07 · url-as-contract** — a public URL is a long-lived contract; changing it requires a redirect,
  not a silent break.
- **co-08 · semantic-html** — landmarks (`nav`/`main`/`article`/`aside`) and their implicit ARIA roles
  serve browsers, crawlers, and assistive tech from one markup source.
- **co-09 · heading-hierarchy** — headings `h1`–`h6` must not skip levels; a single descriptive `h1`
  per page is best practice.
- **co-10 · document-outline** — the nested heading + landmark structure is the machine-readable outline
  of a page.
- **co-11 · xml-sitemap** — a `sitemap.xml` (sitemaps.org protocol) lists canonical URLs with `lastmod`;
  each file caps at 50,000 URLs / 50MB.
- **co-12 · sitemap-index** — a `<sitemapindex>` references multiple sitemap files to exceed the
  per-file cap.
- **co-13 · robots-txt** — the Robots Exclusion Protocol (RFC 9309) serves `/robots.txt` with
  `user-agent`/`allow`/`disallow` rules; an unreachable file means "disallow all".
- **co-14 · meta-robots-noindex** — `<meta name="robots" content="noindex">` and the `X-Robots-Tag`
  header control indexing at page/response granularity (distinct from crawl control).
- **co-15 · canonical-url** — `rel="canonical"` consolidates duplicate URLs onto one representative; it
  is a hint the search engine may override, not a rule.
- **co-16 · crawling-vs-indexing** — crawling (fetching) and indexing (storing/ranking) are separate;
  not every crawled page is indexed.
- **co-17 · crawl-budget** — crawl capacity + crawl demand bound how much a site is crawled; it is a
  large-site (1M+ page) concern, not a small-site worry.
- **co-18 · mobile-first-indexing** — the search engine indexes and ranks the mobile rendering, so
  mobile/desktop content and metadata must match.
- **co-19 · title-meta-description** — the `<title>` and `<meta name="description">` feed the SERP
  snippet; there is no published fixed character limit (snippets truncate to device width).
- **co-20 · structured-data-jsonld** — schema.org vocabularies embedded as JSON-LD make content
  machine-readable and eligible for rich results; markup must match visible content.
- **co-21 · open-graph** — Open Graph `og:title`/`og:type`/`og:image`/`og:url` are the four required
  properties (ogp.me) controlling shared-link previews.
- **co-22 · twitter-cards** — `twitter:card` meta tags select a card type for X/Twitter previews.
- **co-23 · hreflang** — `rel="alternate" hreflang` links declare localized versions; links must be
  bidirectional and include a self-reference plus an `x-default`.
- **co-24 · redirects-301-302-308** — 301 (permanent, passes signals) vs 302 (temporary, keeps source
  indexed) vs 308 (permanent, preserves the HTTP method).
- **co-25 · core-web-vitals-seo** — LCP/INP/CLS form a page-experience signal (one input among many),
  not a standalone ranking factor.
- **co-26 · internal-linking-pagerank** — internal links and anchor text distribute link equity;
  PageRank (Brin & Page, 1998) models the web as a link graph.
- **co-27 · accessibility-seo-overlap** — alt text (WCAG 1.1.1), semantic structure, and ARIA roles
  serve both accessibility and machine legibility from the same markup.
- **co-28 · measuring-search-console** — Google Search Console (coverage, performance, sitemaps) and a
  Lighthouse SEO audit are the primary measurement surfaces.

## Tensions & trade-offs — when NOT to reach for this

- **SEO is not content quality**: perfect markup on thin, unhelpful content still loses. Structured
  data and Core Web Vitals are amplifiers, not substitutes — chasing them for a page nobody wants is
  effort spent on the wrong layer.
- **Structured data has a maintenance and honesty cost**: schema.org markup that drifts from the
  visible page is worse than none — it risks manual penalties and misleads users. Only mark up what's
  genuinely on the page, and only the types you'll keep accurate.
- **Not every surface needs it**: an internal admin tool, a gated app, or an authenticated dashboard
  gains nothing from sitemaps, rich results, or crawl optimization. IA discipline still helps
  navigation, but the SEO machinery is for public, discoverable content only.

## Lineage — why it beat the alternative

- Information architecture matured as library-science practice for the web (the "polar bear book"),
  and early SEO was an arms race of keyword stuffing and link tricks. Search engines responded by
  rewarding what actually helps users: semantic structure, honest metadata, explicit structured data,
  and fast, stable pages. The durable approach won because it aligns the machine's incentives with the
  reader's — structure content well and both crawlers and people benefit, with no penalty risk. This
  hands well-structured, crawlable, performant public surfaces to the operational concerns of
  [topic 47 Advanced Frontend](./advanced-frontend.md) (rendering for crawlability and vitals) and
  builds directly on the semantic-HTML foundation of
  [topic 14 Frontend Essentials](./frontend-essentials.md).

## Worked examples

Colocated under `information-architecture-and-seo/learning/code/`; each artifact is real served markup
(or an annotated IA/decision artifact) checked against crawler/validation tooling (DD-20/DD-30).
Contiguous `ex-01..ex-53`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · ia-four-systems** — annotate a site map labeling its organization, labeling, navigation, and
  search systems — verify all four are named. (co-01)
- **ex-02 · information-scent** — annotate two nav labels, one with strong scent and one opaque — verify
  the strong-scent label predicts its destination. (co-02)
- **ex-03 · card-sort-open** — run an open card sort producing user-driven groupings — verify categories
  emerge from participants, not predefined. (co-03)
- **ex-04 · card-sort-closed** — a closed card sort into fixed categories — verify every card lands in a
  predefined bucket. (co-03)
- **ex-05 · tree-test** — evaluate findability of three items in a proposed hierarchy — verify each
  item's success/fail path is recorded. (co-04)
- **ex-06 · taxonomy-design** — design a category hierarchy for a small site — verify related content
  groups and depth stays shallow. (co-05)
- **ex-07 · url-hyphens** — write URLs using hyphens not underscores as word separators — verify the
  hyphenated form. (co-06)
- **ex-08 · url-readable** — replace an opaque `?id=837` URL with readable words — verify the slug is
  human-legible. (co-06)
- **ex-09 · url-hierarchical** — a hierarchical `/section/subsection/page` scheme — verify the path
  mirrors the taxonomy. (co-06)
- **ex-10 · url-stability** — change a URL and add a redirect preserving the old path — verify the old
  URL still resolves. (co-07)
- **ex-11 · divsoup-to-semantic** — restructure a `<div>`-soup page into semantic HTML — verify
  landmarks replace generic divs. (co-08)
- **ex-12 · landmarks** — add `nav`/`main`/`article`/`aside` landmarks — verify each region has a
  landmark role. (co-08)
- **ex-13 · heading-outline** — build a correct `h1→h2→h3` outline — verify the document outline nests
  cleanly. (co-09, co-10)
- **ex-14 · heading-skip-bug** — flag a page that jumps `h1→h3` — verify the skipped `h2` is reported.
  (co-09)
- **ex-15 · single-h1** — one descriptive `h1` per page — verify exactly one `h1` exists. (co-09)
- **ex-16 · alt-text** — descriptive `alt` for content images and `alt=""` for decorative ones — verify
  each image's alt matches its role. (co-27)
- **ex-17 · nav-landmark-role** — a `<nav>` element's implicit `navigation` role — verify AT exposes it
  as navigation. (co-08, co-27)
- **ex-18 · document-outline-devtools** — inspect the outline and accessibility tree in DevTools —
  verify the rendered outline matches the markup. (co-10)

### Intermediate

- **ex-19 · xml-sitemap** — a valid `sitemap.xml` with `<loc>`/`<lastmod>` — verify it validates against
  the sitemaps.org schema. (co-11)
- **ex-20 · sitemap-limits** — annotate the 50,000-URL / 50MB per-file cap — verify the limits are
  stated correctly. (co-11)
- **ex-21 · sitemap-index** — a `<sitemapindex>` referencing child sitemaps — verify each child is a
  valid `<sitemap>` entry. (co-12)
- **ex-22 · robots-txt-basic** — a `robots.txt` with `user-agent`/`disallow` — verify a crawler honors
  the disallow. (co-13)
- **ex-23 · robots-txt-allow** — an `allow` overriding a broader `disallow` — verify the allowed path
  stays crawlable. (co-13)
- **ex-24 · robots-unreachable-disallow** — annotate the RFC 9309 rule that an unreachable file means
  "disallow all" — verify the rule is stated. (co-13)
- **ex-25 · meta-robots-noindex** — a `<meta name="robots" content="noindex">` tag — verify the page is
  excluded from the index. (co-14)
- **ex-26 · x-robots-tag** — an `X-Robots-Tag: noindex` response header — verify it applies to a
  non-HTML resource. (co-14)
- **ex-27 · canonical-tag** — a `rel="canonical"` link element — verify it points to the representative
  URL. (co-15)
- **ex-28 · canonical-duplicate** — consolidate two duplicate URLs onto one canonical — verify both
  declare the same canonical. (co-15)
- **ex-29 · canonical-hint-not-rule** — annotate that the engine may pick a different canonical — verify
  the "hint not rule" caveat. (co-15)
- **ex-30 · title-tag** — a descriptive `<title>` element — verify it summarizes the page. (co-19)
- **ex-31 · meta-description** — a `<meta name="description">` feeding the snippet — verify it describes
  the page content. (co-19)
- **ex-32 · serp-snippet-annotate** — annotate how title + description render in a SERP snippet — verify
  the mapping is labeled; note no fixed char limit. (co-19)
- **ex-33 · open-graph-tags** — the four required `og:title`/`og:type`/`og:image`/`og:url` — verify all
  four are present. (co-21)
- **ex-34 · twitter-card** — `twitter:card` meta tags — verify the card type is set. (co-22)
- **ex-35 · crawling-vs-indexing** — annotate the crawl→index distinction — verify a crawled-but-unindexed
  case is shown. (co-16)
- **ex-36 · crawl-budget-large-site** — annotate crawl budget as a large-site concern — verify the
  1M-page threshold is noted. (co-17)
- **ex-37 · mobile-first-parity** — ensure mobile and desktop content/metadata match — verify parity of
  a key element. (co-18)
- **ex-38 · url-canonical-consistency** — sitemap, canonical, and internal links all agree on one URL —
  verify the three sources match. (co-06, co-15)

### Advanced

- **ex-39 · jsonld-article** — schema.org `Article` JSON-LD — verify it parses and the type is
  recognized. (co-20)
- **ex-40 · jsonld-breadcrumb** — `BreadcrumbList` JSON-LD — verify the trail matches the URL hierarchy.
  (co-20)
- **ex-41 · jsonld-product** — `Product`/`Offer` JSON-LD — verify required properties are present.
  (co-20)
- **ex-42 · jsonld-matches-page** — JSON-LD whose values match the visible content — verify no
  markup-vs-page drift. (co-20)
- **ex-43 · rich-results-validate** — validate JSON-LD for rich-result eligibility — verify zero errors
  in the validator. (co-20)
- **ex-44 · hreflang-bidirectional** — `hreflang` links listing all versions plus a self-reference —
  verify the links are bidirectional. (co-23)
- **ex-45 · hreflang-x-default** — an `x-default` fallback for unmatched locales — verify the default is
  declared. (co-23)
- **ex-46 · redirect-301** — a 301 permanent redirect — verify it passes signals to the target. (co-24)
- **ex-47 · redirect-302-vs-301** — a 302 that keeps the source indexed — verify the semantic difference
  from 301. (co-24)
- **ex-48 · redirect-308-method** — a 308 that preserves the HTTP method — verify a POST stays a POST.
  (co-24)
- **ex-49 · cwv-measure-seo** — measure LCP/INP/CLS as a page-experience signal — verify the metrics are
  captured and framed as one input among many. (co-25)
- **ex-50 · internal-linking-anchor** — descriptive anchor text distributing link equity — verify anchors
  describe their targets. (co-26)
- **ex-51 · pagerank-annotate** — annotate the PageRank link-graph model — verify the link-graph idea is
  explained. (co-26)
- **ex-52 · search-console-lighthouse** — read a Search Console report and run a Lighthouse SEO audit —
  verify both surfaces report the same page's status. (co-28)
- **ex-53 · seo-capstone** — a machine-legible site: taxonomy + semantic HTML + sitemap/robots/canonical
  - JSON-LD + measured CWV — verify all layers validate together. (co-05, co-08, co-11, co-15, co-20, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a small multi-page site and make it machine-legible end to end — a coherent taxonomy
  and URL scheme, semantic HTML with a correct outline, an XML sitemap + `robots.txt` + canonical
  tags, schema.org JSON-LD for its main content type, and a measured Core Web Vitals pass — validated
  with real tooling.
- **Concepts exercised**: [ ] taxonomy + URL scheme (co-05, co-06) [ ] semantic HTML + document outline
  (co-08, co-09, co-10) [ ] sitemap + robots + canonical (co-11, co-13, co-15) [ ] title/description/Open
  Graph metadata (co-19, co-21) [ ] schema.org JSON-LD (co-20) [ ] Core Web Vitals measurement (co-25).
- **Ordered steps**:
  1. `.../learning/capstone/site/` — restructure pages into semantic HTML with a correct heading
     outline and landmarks. Verify the document outline and accessibility tree in DevTools.
  2. `.../learning/capstone/site/sitemap.xml` + `robots.txt` + canonical tags — declare structure and
     authority. Verify a crawler/validator reads the sitemap and honors canonicals.
  3. `.../learning/capstone/site/structured-data.html` — schema.org JSON-LD for the main content type.
     Verify it passes the structured-data / rich-results validator with no errors.
  4. Measure Core Web Vitals with current tooling and record the result. Verify the primary metrics
     pass and note which rendering choice moved them.
- **Acceptance criteria**: markup is semantic with a correct outline; sitemap/robots/canonicals are
  valid and consistent; JSON-LD validates and matches the visible content; Core Web Vitals pass under
  current tooling.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Information Architecture for the Web and Beyond** — Louis Rosenfeld, Peter Morville, Jorge Arango
  (4th ed., 2015). The standard reference text for information architecture, often called "the polar
  bear book".
- **Don't Make Me Think, Revisited** — Steve Krug (3rd ed., 2014). The classic, widely read primer on
  usability and navigation design.

**Papers & articles**

- **Google Search Central Documentation** — Google (ongoing). The authoritative technical SEO reference
  maintained directly by the search engine it documents. <https://developers.google.com/search/docs>
- **Information Architecture: Study Guide** — Nielsen Norman Group (ongoing). Widely cited
  practitioner-research hub on IA fundamentals, navigation, and findability research methods.
  <https://www.nngroup.com/articles/ia-study-guide/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Quality, product, delivery & leadership — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 14 · Quality, product, delivery & leadership.

> _Content originated in the now-closed FS-SE plan (topic 49); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
