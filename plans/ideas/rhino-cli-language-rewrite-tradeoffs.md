# Evaluate rewriting rhino-cli in .NET (F#) or OCaml for compile-time and disk-usage relief

One-line summary: `apps/rhino-cli` is a ~55,000-line, 183-crate single-binary Rust CLI whose compile
times and shared `target/` disk footprint are a recurring pain point; a `web-researcher` pass found
real, cited evidence that Rust's build cost has a structural cause (monomorphization + per-crate
codegen units) but could not find a single rigorous, same-project benchmark against .NET or OCaml at
this scale — so this brief records the trade-offs found and proposes an empirical spike before any
rewrite decision, rather than deciding from published numbers alone.

> Provenance: surfaced 2026-08-05 from a direct user question ("if I want to rewrite rhino-cli to
> dotnet or ocaml, how much faster will rhino-cli compile?") answered via two `web-researcher` passes
> — one on compile-time/artifact-size/general trade-offs, one specifically on Gherkin/BDD test-runner
> support per language, since `apps/rhino-cli`'s own specs are Gherkin-consumed and any rewrite target
> needs a real story for that. Filed as an idea brief per user instruction, not yet promoted or acted
> on.

## Problem / context

`apps/rhino-cli` is a single Rust binary crate at ~55,000 lines with 183 dependency crates (per
`Cargo.lock`), shared across the `ose-public`/`ose-primer`/`ose-private` byte-identity boundary. Two
concrete costs are already documented elsewhere in this repo's own governance:
[`build-artifact-sweeper.md`](../../repo-governance/development/infra/build-artifact-sweeper.md)
exists specifically because gitignored build output — `target/` chief among them — grows large enough
on the shared machine that an ambient sweeper now deletes it unprompted, and pre-commit/pre-push hooks
that shell out to `cargo run --release` have been observed blocking for tens of seconds to minutes on
cold rebuilds or concurrent-session cargo lock contention this session.

Two independent, cited `web-researcher` passes (2026-08-05) establish:

- **Rust's compile-time and disk-usage costs share one root cause.** The Rust project's own 2026
  roadmap states compile time is "one of the top pain points cited by Rust developers" and that
  "CI pipelines often take 30+ minutes for medium-sized projects"
  ([Fast Builds — Rust Project Goals 2026](https://rust-lang.github.io/rust-project-goals/2026/roadmap-fast-builds.html)).
  A real-world case (Feldera, ~100K generated lines in one crate) took 30-45 minutes to release-build
  until split into 1,106 crates, which cut it to under 3 minutes — because `rustc` parallelizes at
  crate granularity, not within a crate, and rhino-cli is exactly the single-large-crate shape this
  penalizes
  ([HN discussion](https://news.ycombinator.com/item?id=43715235)). The same monomorphization +
  per-crate incremental-caching mechanism that slows builds is what makes `target/` reach 5-15GB for
  actively-developed projects, per the Rust repo's own tracking issue
  ([rust-lang/rust#66348](https://github.com/rust-lang/rust/issues/66348)) and multiple independent
  practitioner write-ups.
- **.NET (C#) compiles meaningfully faster** at comparable scale — a healthy 50-project solution's
  no-change incremental rebuild should be under 2 seconds
  ([9 Things That Silently Kill Your .NET Build Time](https://dev.to/florinvica/9-things-that-silently-kill-your-net-build-time-and-how-to-fix-each-one-3kb4)).
  **F# is measurably slower than C#**, but for a structural reason unrelated to Rust's — F#'s MSBuild
  integration overhead disproportionately exceeds actual compiler time (a small F# project: 3.9s
  compiler time inside a 6.5s total build), per an official `dotnet/fsharp` maintainer discussion that
  includes input from a C# compiler-team member
  ([dotnet/fsharp#11134](https://github.com/dotnet/fsharp/discussions/11134)). No source found gives a
  controlled F# number at rhino-cli's actual scale (55K LOC / 180+ packages) — flagged as a real gap,
  not resolved by extrapolation.
- **OCaml's "fast compiler" reputation is real but uncited at this scale.** Every source treats fast
  OCaml compilation as well-established, uncontested community knowledge, and Dune's own design intent
  is exactly this. But no rigorous, dated, methodologically sound Rust-vs-OCaml compile-time comparison
  at CLI-application scale could be found — the one article with a matching headline was paywalled with
  no visible numbers. This is the single largest evidentiary gap in the research.
- **Disk-usage claims are not apples-to-apples across languages.** Rust's 5-15GB `target/` figure is a
  single-project, actively-developed-project figure. The one comparable .NET number found (40GB) comes
  from long-term multi-project, multi-target-framework accumulation with imperfect `dotnet clean` —
  a different failure mode, not a controlled same-day comparison. No OCaml `_build/` size figure was
  found at all; directional reasoning (no monomorphization, no per-codegen-unit caching) suggests it
  should be smaller than Rust's, but this is inference, not measurement.

## Why now

Nothing is broken today — this is not an incident brief. It is filed now because the question was
asked directly, the research is fresh and cited, and letting it evaporate in chat would mean the next
person to ask the same question (about a tool three repos depend on byte-identically) re-does the same
two research passes from scratch.

## Prior art / precedents

- [`build-artifact-sweeper.md`](../../repo-governance/development/infra/build-artifact-sweeper.md) —
  documents the ambient sweeper that exists because of Rust `target/` growth; this brief's disk-usage
  findings are the root-cause detail behind why that convention was needed at all.
- [`tri-repo-rhino-cli-byte-identity-gate`](./tri-repo-rhino-cli-byte-identity-gate.md) — any rewrite
  decision must account for `apps/rhino-cli` being byte-identical across `ose-public`, `ose-primer`,
  `ose-private` with zero carve-outs, plus a `beaver-nest` fork; a language rewrite is a four-repo
  event, not a one-repo one, by the same boundary this idea already tracks.
- [`rust-crate-structural-checklist-promotion`](./rust-crate-structural-checklist-promotion.md) — a
  cheaper, non-rewrite lever already on record: splitting a monolithic Rust crate into a workspace of
  smaller crates is exactly the change that gave Feldera its 10-15x build-time win, and is a much
  smaller bet than a full-language rewrite.
- **F# already runs in production** for two backends in this repo (`ose-be`, `organiclever-be`), per
  `AGENTS.md`'s Web Sites table — the only one of the three candidate languages with any existing team
  familiarity, which every other section of this brief treats as a real, not incidental, factor.

## Proposed direction (sketch)

Do not rewrite yet. Instead:

1. **Run a build-timing baseline on the current Rust CLI first**, using
   [`cargo build --timings`](https://doc.rust-lang.org/cargo/reference/timings.html) (official,
   built into Cargo) to get a real Gantt-chart profile of rhino-cli's own clean and incremental builds
   — the one number this brief is missing that costs nothing to obtain, since no published benchmark
   substitutes for measuring the actual codebase.
2. **Try the cheap, non-rewrite Rust fixes before evaluating a rewrite**: split rhino-cli into a
   workspace of smaller crates (the single highest-leverage, cited fix — 10-15x in the Feldera case),
   switch to `mold`/`lld` for linking, add `sccache`, and strip debug info in dev builds. These target
   the exact same root cause (monomorphization + per-crate codegen units) a rewrite would sidestep, at
   a fraction of the risk.
3. **If a rewrite is still on the table after step 2**, spike a real slice — port one subcommand plus
   its git/YAML/Markdown dependencies to F# (not OCaml; see Risks) — and measure clean + incremental
   build time and artifact size directly, rather than deciding from the published numbers in this
   brief, none of which are controlled same-project comparisons.

### Gherkin/BDD support per candidate language

`apps/rhino-cli` specs live under `specs/` as Gherkin, consumed by
[`test-driven-development.md`](../../repo-governance/development/workflow/test-driven-development.md)
and [`feature-change-completeness.md`](../../repo-governance/development/quality/feature-change-completeness.md)'s
mandatory coverage rule. A second `web-researcher` pass (2026-08-05) found real maturity differences:

- **Rust**: the `cucumber` crate (cucumber-rs) is actively maintained — v0.23.0 released 2026-04-23,
  ~275K downloads/month, used by 108+ downstream crates — and its companion `gherkin` crate is a pure
  Rust Gherkin parser covering most of the language, with one narrow documented quirk (Scenario Outline
  parsed the same as Outline/Example)
  ([cucumber-rs/gherkin CHANGELOG](https://github.com/cucumber-rs/gherkin/blob/main/CHANGELOG.md)).
  It is async-first (requires a `tokio` runtime and a `harness = false` test target), which is
  architectural overhead but not a blocker. Per prior-session memory, wiring this up for rhino-cli's
  own specs is already tracked as deferred future work, independent of this brief.
- **.NET**: SpecFlow (the long-standing .NET Cucumber implementation) is superseded by **Reqnroll**,
  forked by SpecFlow's original creator and actively maintained (releases roughly every 4-8 weeks,
  latest v3.3.4 as of 2026-03-23, including a prompt CVE patch)
  ([Reqnroll — From SpecFlow to Reqnroll](https://reqnroll.net/news/2024/02/from-specflow-to-reqnroll-why-and-how/)).
  F# step definitions are supported, but with a structural catch: feature files must be hosted in a
  C#/VB project, with F# plugged in as an "external binding assembly" — not a pure single-language F#
  setup
  ([Reqnroll F# Support](https://docs.reqnroll.net/latest/integrations/fsharp.html)).
- **OCaml**: the one real option, `cucumber.ml` (the official Cucumber-org OCaml implementation), was
  **archived by its owner on 2026-02-16** and is now read-only. It also depended on a compiled C
  library (`libgherkin.so`) rather than being pure OCaml, and had low community investment even before
  archival (29 stars, 3 open issues) ([cucumber/cucumber.ml](https://github.com/cucumber/cucumber.ml)).
  No maintained alternative surfaced across multiple targeted searches — this is a real, cited
  disqualifier for OCaml given the repo's hard Gherkin-consumption requirement, independent of any
  compile-time advantage OCaml might have.

## Rough scope & non-goals

In scope: recording the compile-time, disk-usage, general trade-off, and Gherkin-support findings as a
citable reference; proposing the spike-before-rewrite sequencing.

Out of scope:

- Actually rewriting any part of `rhino-cli` — this brief makes no rewrite decision.
- Running the proposed `cargo build --timings` baseline or the F# spike — both are next steps if this
  idea is promoted, not part of this filing.
- Deciding the non-rewrite Rust fixes (crate-splitting, `mold`/`sccache`) — those could be pursued
  independently of this brief's rewrite question entirely, and are only cross-referenced here as a
  cheaper alternative.
- Re-litigating the four-repo byte-identity boundary — tracked separately by
  [`tri-repo-rhino-cli-byte-identity-gate`](./tri-repo-rhino-cli-byte-identity-gate.md).

## Risks & open questions

- **The core evidentiary gap: no same-project benchmark exists for any of the three languages at
  rhino-cli's actual scale.** Every number in this brief is either official/structural (why Rust is
  slow) or drawn from a different-sized project. Deciding a rewrite from these numbers alone would be
  deciding on inference, not measurement — hence the proposed spike. (open)
- **OCaml carries two independent disqualifying signals** for this specific repo: no maintained Gherkin
  runner (hard requirement), and — from the general trade-off research — `omd`, OCaml's markdown
  library, is itself flagged as "seeking a new maintainer," a second maintenance-risk signal
  landing directly on a stated rhino-cli dependency (markdown parsing). Both make OCaml a materially
  weaker candidate than F# for this codebase specifically, independent of any compile-time win it might
  offer. (leaning resolved — OCaml likely not worth spiking given these two disqualifiers, F# is)
- **A rewrite is a four-repo event**, not a one-repo one, given the byte-identity boundary; the
  `beaver-nest` fork adds a fifth surface with its own drift risk. Scope and cost multiply accordingly
  if this is ever promoted. (open)
- **F#'s AOT/reflection-heavy-serialization risk**: `YamlDotNet` now ships an AOT source generator, so
  the ecosystem has caught up, but any F# spike needs to deliberately choose AOT-compatible libraries
  rather than defaults, per the general-trade-off research. (open, addressed by spike design)
- **Team familiarity is a real, not incidental, factor already in this repo's favor for F#** — two
  backends already run F# in production — but this brief does not know whether the maintainer weighs
  that advantage enough to outweigh a 55K-line rewrite's cost and risk. (open)

## What success looks like + promotion signal

Success for this brief alone is narrow: the trade-offs and gaps found are recorded once, citably, so
neither a future session nor a future contributor re-runs the same two research passes from scratch.

Promotion signal: the maintainer wants either (a) the non-rewrite Rust fixes pursued as their own
scoped plan (crate-splitting, linker/cache tuning) independent of any rewrite question, or (b) the
`cargo build --timings` baseline plus an F# spike run for real, at which point this brief promotes into
a backlog plan carrying real, same-project numbers instead of the cross-project inferences recorded
here.
