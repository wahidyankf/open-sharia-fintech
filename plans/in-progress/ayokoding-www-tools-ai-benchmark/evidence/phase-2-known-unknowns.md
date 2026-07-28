# Phase 2 — Known-unknowns resolution record (K-1 … K-8)

> Snapshot: 2026-07-28. This file records the terminal state of every known unknown carried into
> execution from [`tech-docs.md` §"Known unknowns carried into execution"](../tech-docs.md). Each
> gap was resolved against a **primary** source where one existed; whichever remained unresolved is
> transcribed into `models.ts` with grade `unavailable` or `conflicted` — never guessed. The two
> transcription hazards (Cursor Composer 2.5's version-trap figures) are recorded at the foot of
> this file because they became dataset invariant 9.

## Resolution table

| #   | Gap                                                                                        | Resolution                                                                                                                                                                                                                                                                                                                                        | Landing in `models.ts`                                             |
| --- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| K-1 | Claude Opus 5 Terminal-Bench 2.1 — not captured                                            | No primary or secondary figure found. The Opus anchor's coverage stays at SWE-bench Verified + GPQA Diamond (weight 55 / coverage 0.55).                                                                                                                                                                                                          | Absent (no `terminal-bench-2-1` figure on `claude-opus-5`).        |
| K-2 | Claude Opus 5 GPQA Diamond — three conflicting secondary figures (93.2–94.3)               | Three sources, three numbers, no primary retrievable. Grade `conflicted`; the **LOW** value (93.2) enters the composite, full range 93.2–94.3 stored. Source: `https://platform.claude.com/docs/en/models/overview` (no primary resolves).                                                                                                        | `cf("gpqa-diamond", 93.2, 94.3, …)` on `claude-opus-5`.            |
| K-3 | GPT-5.6 SWE-bench Verified — vendor does not report; one aggregator figure looks erroneous | Vendor moved to SWE-bench Pro. The aggregator's **96.2% is NOT transcribed** — it is contradicted by the better source. Grade `unavailable`; no `swe-bench-verified` figure on any GPT-5.6 model.                                                                                                                                                 | Absent on `gpt-5.6-sol/terra/luna`.                                |
| K-4 | Grok 4.5 and Kimi K3 GPQA / AIME — vendors omit                                            | Grok 4.5 GPQA not published by the vendor; no figure transcribed (grade `unavailable`, absent). Kimi K3 GPQA **is** published (93.5%, secondary) and is transcribed; AIME is not a composite benchmark (rejected), so its omission has no impact.                                                                                                 | Grok 4.5 GPQA absent; Kimi K3 GPQA present.                        |
| K-5 | LMArena current Elo — board unsettled                                                      | No impact. LMArena is **not** in the composite (measures stylistic preference; board in flux).                                                                                                                                                                                                                                                    | n/a — LMArena is never transcribed.                                |
| K-6 | Kimi K2.7 Code pricing — official page did not return content                              | Official Moonshot page (`https://platform.kimi.ai`) did not return content. OpenCode Zen lists K2.7-code at `$0.95/$4.00` (passthrough) — recorded as grade **`secondary`** (not the primary vendor rate). The model still appears with its roster/pricing data; the official direct rate remains unresolved. Source: `https://opencode.ai/docs`. | `met(0.95, 4, "secondary", …)` on `kimi-k2.7-code` (Zen + Cursor). |
| K-7 | Artificial Analysis ToU exact republication clause — PDF not text-extractable              | No impact. Artificial Analysis is **not** used as a data source — only cited as prior art (the worked example, A.5, attributes its Coding Agent Index rather than copying figures).                                                                                                                                                               | n/a — Artificial Analysis figures are not transcribed.             |
| K-8 | Terminal-Bench and ARC Prize republication terms — not stated by either                    | No terms stated by either operator. The page's Sources and Licences section records "no terms stated" rather than implying permission; figures are cited (with source URLs) under standard scholarly attribution, not re-licensed.                                                                                                                | n/a — disclosure only.                                             |

## Transcription hazards → invariant 9

Two hazards found in the research are encoded as dataset invariant 9 ("no model carries a
Terminal-Bench 2.0 or SWE-bench Multilingual figure in a 2.1 or Verified field"):

- **Cursor Composer 2.5's 79.8%** is SWE-bench **Multilingual** — a different benchmark. It must
  never land in the `swe-bench-verified` column. → **Not transcribed**; Cursor Composer 2.5 carries
  no `swe-bench-verified` figure.
- **Cursor Composer 2.5's 69.3%** is Terminal-Bench **2.0**, not 2.1. → **Not transcribed**; the
  model carries no `terminal-bench-2-1` figure. Terminal-Bench 2.0 and 2.1 are not interchangeable,
  and SWE-bench harness releases 1.x and 2.x are explicitly not comparable.

Consequence: Cursor Composer 2.5 has **no** composite-benchmark figures → coverage 0 → `unrated`
band. Its roster entry, Cursor-standard pricing (`$0.50/$2.50`), and the A.5 worked-example cost
advantage are still shown.

## Figures that could not be sourced from Appendix A

Two roster models with benchmark data have **no transcribable standard-tier price** in Appendix A.4
(A.4 prices the Gemini 3.6/3.5 Flash line and the 2.5 line, but not these). Rather than invent a
number, the price set is omitted for these models while their benchmark data is retained:

- **Gemini 3.1 Pro** — `pricing: {}`. Benchmark figures (SWE-V self-reported 80.6, GPQA conflicted
  94.1–94.3) retained.
- **Gemini 3 Flash** — `pricing: {}`. Benchmark figure (SWE-V conflicted 76.2–78.0) retained.

These omissions are caught by neither the price-source invariant (an empty price set has no price
figures to source) nor the page's honesty surface beyond coverage; they are flagged here so a future
refresh can fill them from Google's pricing page when the rate is published.
