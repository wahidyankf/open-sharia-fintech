---
description: The four content standards governing what may and may not appear in a Why It Matters section
when_to_use: Read this to check whether a specific sentence in a Why It Matters section is a prohibited or permitted pattern.
---

# Standards

## Standard 1: Theoretical Explanations Only

Every `**Why It Matters**:` section MUST rely solely on:

- Statements about the concept or pattern as a general category
- Capability claims: what the pattern enables, prevents, or guarantees
- Trade-off discussions: what is gained and what is sacrificed
- References to verifiable technical facts — library names, algorithm complexity,
  language specifications, or industry-standard definitions with citable sources

## Standard 2: Prohibited Content Patterns

The following patterns are **never** permitted inside a `**Why It Matters**:` section:

**Prohibited: Named-company anecdotes**

Any sentence that names a specific company (Netflix, Amazon, LinkedIn, Uber, Google,
Stripe, Shopify, Coinbase, PayPal, Facebook, Twitter, Apple, Microsoft, etc.) in
connection with an internal engineering decision, migration, or metric.

**Prohibited: "When [Company] did X" structure**

Sentences following the pattern: _"When [Company] implemented / migrated / adopted /
refactored X, they achieved / reduced / improved Y."_

**Prohibited: Fabricated platform scenarios**

Sentences that replace a company name with a generic category to preserve the anecdotal
structure: _"A ride-sharing platform...", "A large e-commerce company...", "A fintech
startup..."_ These patterns fabricate a scenario to simulate evidence without providing
any.

**Prohibited: Unsourced numeric claims**

Specific percentages, counts, cost savings, or performance ratios attributed to a
real or implied organization without a citable primary source (engineering blog post,
academic paper, official announcement, or conference talk with a URL).

## Standard 3: Suspension Test

Before writing any sentence containing a company name or a specific metric, ask:
**"Can I link to the primary source right now?"**

- If yes: include the inline link and write the claim. The claim is now verifiable.
- If no: rewrite using the underlying principle without the company name and metric.

This test applies to both human authors and AI content agents.

## Standard 4: Permitted Reference Patterns

The following reference patterns are permitted because they are verifiable:

| Pattern                              | Example                                                                                                           |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------- |
| Citable historical fact with source  | "Tony Hoare called null references his 'billion-dollar mistake' (QCon 2009)"                                      |
| Named tool with documented behaviour | "Netflix's Hystrix popularized circuit breakers; it is now in maintenance mode"                                   |
| Well-known community-verified event  | "Twitter's Finagle directly influenced the creation of Linkerd (now a CNCF project)"                              |
| Academic or specification reference  | "Dijkstra's seminal 1968 letter, 'Go To Statement Considered Harmful'"                                            |
| Mathematical property statement      | "N states × M variants without parameterization = N×M total states"                                               |
| General pattern consequence          | "Without explicit state machine enforcement, nothing prevents an order from being marked 'shipped' before 'paid'" |
