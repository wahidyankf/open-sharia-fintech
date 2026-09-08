---
description: The dotfile-shaped rule that lets a non-dotfile <word>.env course fixture under apps/<app>/content/** bypass guard-env-file-access.
when_to_use: Use when a course or teaching-material app needs to ship a worked-example env file and you need to know whether it is exempt from the agent-access guard.
---

# Content-Fixture Exclusion

Course and teaching material sometimes ships an env file as a **worked example** — an
ayokoding-www self-hosting kata that demonstrates a secret committed to a repo, for instance. Those
files are published curriculum, not real environment files, and blocking them stops agents from
authoring, linting, or even `git stash`-ing the course they belong to.

A file is excluded from `guard-env-file-access` when **both** hold:

1. It lives under an app's published content tree — `apps/<app>/content/**`.
2. Its basename ends in `.env` and is **not** a dotfile — `kata.env`, `app.env` qualify;
   `.env`, `.env.local` do not.

Everything else stays denied. A dotfile `.env*` under `content/` is still denied, and a
`<word>.env` outside any content tree is still denied.

**The exclusion is expressed by pattern shape, not by an enumerated path list.** Every guard keys on
a **dotfile** basename — `.env`, `.env.local` — so a `<word>.env` fixture falls outside the deny
without any per-tree entry. A new content tree needs no configuration change.
