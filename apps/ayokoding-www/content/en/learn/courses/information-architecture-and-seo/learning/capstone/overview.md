---
title: "Discoverability Capstone"
date: 2026-07-31T00:00:00+07:00
draft: false
weight: 1
---

The capstone assembles one small public-content surface from semantic HTML, stable URLs, a canonical
link, JSON-LD, an XML sitemap, and crawler directives. Its acceptance bar is that a reader, screen
reader, and crawler receive consistent structural information from the same source artifacts.

## Run and inspect

1. Serve [the capstone site](./site/index.html) with a local static server.
2. Inspect its landmarks, one-page-topic heading, title, description, canonical URL, and JSON-LD.
3. Parse [sitemap.xml](./site/sitemap.xml) and compare its URL with the canonical and internal link.
4. Review [robots.txt](./site/robots.txt) and [metrics.json](./site/metrics.json) as the crawler-policy
   and measured-experience evidence.

The capstone uses the reserved `example.test` domain so it remains safe to inspect locally without
claiming a live public deployment or a rich-result guarantee.
