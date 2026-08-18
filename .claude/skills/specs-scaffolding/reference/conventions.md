# Conventions Followed

## PM-Readability Contract

Every file created under `specs/apps/` includes the required header block:

```markdown
# <Title>

> **Audience**: Engineers, Technical Product/Project Managers
>
> **Plain-language summary**: <one paragraph; no un-glossed niche terms>

## <First section heading>
```

Niche terms (F#, Giraffe, PGlite, XState, Effect TS, bounded context, aggregate, ubiquitous
language) are glossed on first use within each file. Mainstream SWE vocabulary (TypeScript,
Next.js, Postgres, REST, OpenAPI, Docker, etc.) is never glossed.

See [App README vs Specs Convention](../../../../repo-governance/conventions/structure/app-readme-vs-specs.md)
Standard 5 for the complete PM-readability contract.

## Feature File Placement

BE/web/CLI: MUST be placed in domain subdirectories under `behavior/<surface>/gherkin/<domain>/`
(all surfaces use the same domain-subdir rule; build-time CLI features share the `cli` surface).
Libs: MUST be placed in package subdirectories under `gherkin/<package>/`.

See [Specs Directory Structure Convention](../../../../repo-governance/conventions/structure/specs-directory-structure.md)
for full rules.

## README Structure (Spec Area Root)

1. Title and plain-language summary (PM-readability header block).
2. Surface profile note (what folders are present and why).
3. Folder table (folder name, purpose, contents summary).
4. Relationship to app READMEs (link to `apps/<app>/README.md`).
5. Related links (governance conventions, spec validation workflow).

## Background Steps (by surface)

- BE specs: `Given the API is running`
- Web specs: `Given the app is running`
- CLI specs: `Given the CLI is installed`
- Library specs: `Given the library is imported`

## Folder Listing Order

In any README listing, folders appear in canonical order: `product/`, `system-context/`,
`containers/`, `components/`, `behavior/`.
