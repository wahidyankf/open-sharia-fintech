# BeaverNest first LLM integration

One-line summary: give `beavernest-be` its first real AI-assistant capability — currently there is
no capture, no notes, no LLM calls, and no prompt plumbing at all.

> Idea, added 2026-07-31, filed from `beaver-nest`'s `baseerah-repo-reset` plan's Product Scope §
> Out of scope. Carried into `ose-public` 2026-08-10 by the `beaver-nest-repo-consolidation` plan's
> idea-triage step as part of the BeaverNest product port; renamed from
> `beaver-nest-first-llm-integration` to `beavernest-first-llm-integration` to match this repo's
> single-token domain naming
> ([File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md)).

## Problem / context

`beaver-nest`'s `baseerah-repo-reset` scoped `beaver-nest-be`/`beaver-nest-fe` (now
`beavernest-be`/`beavernest-app`) as a pure hello-world walking skeleton: "Every product feature
[is out of scope]. No capture, no notes, no LLM calls, no prompt plumbing, no AI SDK dependency, no
scheduling, no posting." That was correct for establishing the engineering harness, but it means
none of BeaverNest's actual stated purpose — an AI assistant, per
[BeaverNest — Product](../../../specs/apps/beavernest/product/README.md) — exists yet.

## Why now

Not yet — this is a placeholder for the plan that picks the first concrete AI-assistant capability
to build. Choosing a provider/SDK before a feature is scoped would be speculative.

## Prior art / precedents

- [BeaverNest — Product](../../../specs/apps/beavernest/product/README.md) — scopes the product to
  assistant work, content building, posting, and personal workflow automation; this idea is the
  first slice of the assistant facet, listed there as the Assistant Core deferred capability.
- `vercel:ai-architect` agent (already available in this repo's agent roster) — specializes in
  architecting AI-powered applications, choosing AI SDK patterns, and configuring providers; the
  natural agent to drive this once scoped.
- [beavernest-persistence-layer](./beavernest-persistence-layer.md) — an LLM integration that needs
  to remember anything (conversation history, captured notes) depends on this idea landing first or
  alongside it.

## Proposed direction (sketch)

- Pick one small, concrete first capability (e.g., a single free-text capture endpoint that an LLM
  summarizes or tags) rather than building general-purpose prompt plumbing up front.
- Use the Vercel AI SDK, consistent with the `vercel:ai-architect` agent already in this repo's
  toolset and with the `[domain]-be` backend pattern.

## Rough scope & non-goals

In scope: eventually, the first LLM-backed route in `beavernest-be`.

Out of scope (for now): choosing a specific model/provider, prompt design, or any persistence for
LLM output — those depend on the concrete feature this idea is deferred until.

## Risks & open questions

- Which capability is the first LLM-backed feature — capture, notes, or something else? (open —
  determines the whole shape)
- Does this depend on [beavernest-persistence-layer](./beavernest-persistence-layer.md) landing
  first, or can a stateless first LLM call (no storage) ship independently? (open)
- Provider choice and cost/rate-limit implications for a personal-use product? (open)

## What success looks like + promotion signal

Success: `beavernest-be` serves one real LLM-backed route, however small. Ready to promote once a
maintainer picks the first concrete AI capability to build — until then it correctly stays an
under-specified idea.
