---
title: "Overview"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

**Q1.** What makes a URL an information-architecture contract?

<details>
<summary>Answer</summary>

Readers, bookmarks, links, and crawlers rely on its stable meaning; a changed public URL needs an
appropriate redirect rather than a silent break.

</details>

**Q2.** What is the difference between crawling and indexing?

<details>
<summary>Answer</summary>

Crawling fetches a URL; indexing stores and evaluates content for retrieval. A fetched page is not
automatically included in an index.

</details>

## Scenario Judgment

1. A product page has an image containing meaningful price information but uses an empty alt attribute.
2. Two URLs show the same article and both can be crawled.
3. An internal authenticated dashboard is absent from a sitemap.

<details>
<summary>Answer</summary>

The image needs an equivalent text alternative; the duplicate pages need an intentional canonical
strategy; and the dashboard should remain outside public-search optimization unless it becomes a public
surface.

</details>

## Hands-On Repetition

1. Inspect a page's landmark and heading outline with browser accessibility tooling.
2. Validate the course sitemap and JSON-LD artifacts locally.
3. Review a redirect, canonical link, and robots rule as one crawlability decision.
