# Learnings — web-ui Code-Block Copy Button

> Transient running log the executor appends to during delivery: one entry per generalizable learning,
> sanitized per the secret/sensitivity gate BEFORE it is ever written. Triaged to a durable home (or an
> explicit discard) in the Knowledge Capture phase before archival. If nothing generalizable surfaced,
> record the explicit `No generalizable learnings — <reason>` escape rather than leaving this empty.

## Entry template

```markdown
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
- **Routing (filled at Knowledge Capture)**: <durable home | backlog plan slug | discarded: reason>
```

## Candidate watch-items (delete if they do not materialize)

- Whether `getTextContent` over `rehype-pretty-code` per-line spans preserves newlines verbatim, or
  whether the per-`[data-line]` `\n`-join contingency was needed (see `tech-docs.md`). If the contingency
  fired, this is a reusable extraction insight for any future clipboard-from-highlighted-HTML feature.
- Whether the new `role=status aria-live=polite` sr-only pattern should be promoted to a shared web-ui
  live-region helper for reuse beyond `CopyButton`.
- Any jsdom `navigator.clipboard` stubbing friction worth codifying in the web-ui testing docs.

## Entries

_(none yet)_
