---
description: How to recognize invented corporate metrics in Why It Matters sections, the confirmed fabricated examples found in this codebase, and what content is prohibited vs. allowed.
when_to_use: Use when writing or reviewing a Why It Matters section that names a real company alongside a specific metric or outcome.
---

# Fabricated Corporate Case Study Rule — The Pattern and What's Allowed/Prohibited

See [Detection and Remediation](./fabricated-case-study-detection-and-remediation.md) for the suspension test, checker detection pattern, and how to fix a fabricated claim.

## The Pattern

Tutorial "Why It Matters" sections frequently contain fabricated corporate anecdotes with specific metrics:

> "When [Company] implemented [pattern], they reduced [metric] by [specific %]."

These appear credible because they use real company names and plausible technology. They are almost always invented. No primary source (engineering blog, academic paper, conference talk) exists for them — the absence of any trace across extensive web search is a strong fabrication indicator.

**Confirmed fabricated examples found in this codebase:**

- "Netflix recommendation accuracy improved from 65% to 82% via DDD Ubiquitous Language"
- "Shopify reduced order-related bugs by 73% after anemic→rich model refactor"
- "Coinbase used Event Sourcing temporal queries during an IRS audit"
- "LinkedIn's job application FSM had 150+ states, compressed to 15, saving 18GB memory across 1.7M applications"
- "Shopify product availability FSM saved $120K/month in database costs"
- "PayPal early payment system had 10 TPS limit, increased to 10,000 TPS by switching to eventual consistency"

## What Is Prohibited

**Never write "Why It Matters" using:**

- A real company name + a specific metric (%, count, dollar amount, timing ratio) without a citable primary source
- Statistics that read as plausible but have no engineering blog post, paper, or official documentation behind them
- Narratives where a company "discovered," "measured," or "documented" an internal result that is never cited
- Fabricated precision: "30%", "15 service classes", "120/month reduced to 12" are all hallmarks of invented statistics

## What Is Allowed

**"Why It Matters" should use:**

| Allowed                                        | Example                                                                                                                           |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| General architectural principle with rationale | "Without explicit state machine enforcement, nothing prevents an order from being marked 'shipped' before 'paid'"                 |
| Documented real company fact with attribution  | "NASA's Mars Climate Orbiter ($327M total mission cost) was lost due to a unit mismatch — pound-force seconds vs. newton-seconds" |
| Citable research with clear attribution        | "Tony Hoare called null references his 'billion-dollar mistake'"                                                                  |
| Documented tool/feature from official sources  | "Netflix's Hystrix popularized circuit breakers; it is now in maintenance mode"                                                   |
| Mathematical inevitability                     | "N states × M variants without parameterization = N×M total states"                                                               |
| Well-known community-verified facts            | "Twitter's Finagle directly influenced the creation of Linkerd (now a CNCF project)"                                              |
