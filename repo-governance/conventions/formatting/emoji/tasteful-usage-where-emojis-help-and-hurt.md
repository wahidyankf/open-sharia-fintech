---
description: The jobs emojis can usefully do (section markers, status indicators, navigation signposts) versus the anti-patterns that add visual noise without benefit.
when_to_use: Use when deciding whether adding an emoji to a specific spot in a document will help or hurt scannability.
---

# Tasteful Usage: Where Emojis Help and Hurt

Emojis in this repository are **allowed** across documentation (see Usage Rules for the full path list), but permission to use does not mean obligation to use. The goal is scannability — helping readers locate content quickly — not decoration. Tasteful usage aligns with the [Documentation First](../../../principles/content/documentation-first.md) and [Progressive Disclosure](../../../principles/content/progressive-disclosure.md) principles: emojis must earn their place by adding semantic value, and a reader should grasp the same structure even with emojis stripped.

## Where Emojis Help

Emojis pay for themselves when they do one of these jobs:

- **Section markers in long docs** — a single emoji at the start of an H2/H3 in a 500+ line reference or explanation speeds location-finding on re-read
- **Status indicators in examples** — PASS `✅` / FAIL `❌` / warning `⚠️` inline in "good vs bad" examples or plan status lines
- **Navigation signposts in READMEs** — one emoji per top-level section in a README index (Overview, Quick Start, Docs, Contributing)
- **Plan status in checklists** — `✅` for completed milestones, `🚧` for in-progress, `⏳` for upcoming in plan delivery sections
- **Criticality or severity tags** — 🟠 HIGH / 🟡 MEDIUM / 🟢 LOW already used in agent and Skill definitions

## Where Emojis Do NOT Help (Anti-Patterns)

These patterns are forbidden because they add visual noise without navigation benefit:

- ❌ **Every bullet prefixed with an emoji** — turns a list into a wall of icons; nothing stands out
- ❌ **Emojis inside headings on every page section** — if every H2 is emoji-prefixed, emoji loses its "look here" signal
- ❌ **Decorative emojis with no semantic purpose** — `🎉 Welcome!`, `🌟 Features`, `🚀 Performance` used purely as ornament
- ❌ **Emoji as a bullet substitute** — replacing `-` with `👉` or `🔹`; Markdown already has bullets
- ❌ **Stacked emojis for emphasis** — `## 🔥🔥 Important 🔥🔥`
- ❌ **Emoji in body text for mood** — "This is cool 😎" or "Fixed 🎊"
