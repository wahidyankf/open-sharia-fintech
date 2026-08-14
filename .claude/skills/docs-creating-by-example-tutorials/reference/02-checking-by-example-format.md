# Checking By Example Format

Validation checklist for `apps-ayokoding-www-by-example-checker`.

## 1. Example Count

Minimum 75 annotated code examples, target 75-85. Each example follows the five-part structure.

## 2. Annotation Density

**CRITICAL**: 1.0-2.25 comment lines per code line PER EXAMPLE (not tutorial-wide average).
Comments explain WHY, not WHAT. Flag if density <1.0 (under-annotated) or >2.5 (over-annotated).

**Formula direction** (critical to get right):

```python
# CORRECT
density = comment_lines / code_lines
# Example: 10 comments / 5 code lines = 2.0 -> PASS (within 1.0-2.25)

# WRONG — inverted
density = code_lines / comment_lines  # 5 / 10 = 0.5 would incorrectly flag as FAIL
```

**Counting rules**: code lines are actual executable code (excluding blank and full-comment-only
lines); comment lines contain annotation markers (`// =>`, `# =>`, `-- =>`, `;; =>`), counting both
inline and full-line comments plus multi-line `// =>` continuations as separate lines; density is
calculated per example individually, never as a file average.

## 3. Structure

Five-part structure for each example: (1) Brief Explanation (2-3 sentences), (2) Mermaid Diagram
(when appropriate), (3) Heavily Annotated Code (1.0-2.5 density), (4) Key Takeaway (1-2 sentences),
(5) Why It Matters (50-100 words; flag if >100).

## 4. Self-Containment

Examples runnable within chapter scope (copy-paste-runnable), full imports present, helper
functions included in-place, no external references required, self-contained even while building
on earlier concepts.

## 5. Example Grouping

Thematic grouping (Basic, Error Handling, Advanced, etc.), progressive complexity within groups,
clear group headers.

## 6. ayokoding-web Compliance

Per `apps-ayokoding-www-developing-content`: bilingual content (id/en), content structure and
metadata, linking conventions.

## 7. Diagram Count

Total 30-50 across all levels (~35-60% of 75-85 examples): beginner 7-11 (25-37%), intermediate
8-17 (30-60%), advanced 10-24 (40-86%). Color palette: Blue `#0173B2`, Orange `#DE8F05`, Teal
`#029E73`, Purple `#CC78BC`, Brown `#CA9161`. Appropriate usage only for complex concepts (data
flow, state machines, concurrency).

## 8. Core Features First Principle

**Beginner** (CRITICAL): count external dependencies (imports not in standard library) — flag any
present, should be zero. External dependency = requires installation (npm/pip/Maven/etc.).
**Intermediate** (HIGH): for each dependency, check for a "Why Not Core Features" explanation —
flag if introduced without justification. **Advanced** (MEDIUM): check for trade-off comparisons
(core vs. external) and performance/complexity justifications.

## 9. Examples-by-Level Section in Overview (CRITICAL)

See the [Examples-by-Level Section rule](../../../repo-governance/conventions/tutorials/swe-by-example.md#examples-by-level-section-mandatory)
for the full standard. For each tutorial's `overview.md`:

1. **Presence** — MUST contain an `## Examples by Level` heading. Flag CRITICAL if absent.
2. **Coverage** — every `### Example N: Title` heading on every level page (`beginner.md` /
   `intermediate.md` / `advanced.md` / `production.md`) MUST appear as exactly one bullet. Flag
   CRITICAL for any missing or extra example.
3. **Verbatim text** — bullet link text MUST equal the heading text character-for-character. Flag
   HIGH for any divergence.
4. **Slug correctness** — anchor MUST equal `github-slugger`'s slug of the same heading; sanity-check
   via `node -e "import('github-slugger').then(m => console.log(new m.default().slug('<heading>')))"`.
   Flag HIGH for any mismatch.
5. **Path correctness** — link path MUST be `/en/learn/...<tutorial-base>/<level>` (no trailing
   slash, lowercase level). Flag MEDIUM for malformed paths.
6. **Subsection headings** — MUST be `### {Beginner|Intermediate|Advanced|Production} (Examples
N–M)` (en-dash, not hyphen). Flag LOW for deviations.

If the link checker (`ayokoding-cli`) is wired to validate anchors, also flag any bullet pointing
to a non-existent anchor (CRITICAL).

## Step-by-Step Validation Order

Count examples (flag if <75) → validate annotation density per example → validate five-part
structure → validate grouping → validate ayokoding-web compliance → validate Core Features First
per level → count and validate diagrams → validate the Examples-by-Level section → finalize report
with prioritized summary.
