# fsharp-crane-core Specs

The behavioral corpus for
[fsharp-crane-core](../../../libs/fsharp-crane-core/project.json), the shared F# domain core for
PDF-to-Markdown conversion and verification.

A library owns exactly one surface, so the three corpus entries sit directly under the library
root rather than under an owner directory — see
[Logical Owner Corpus](../../../repo-governance/conventions/structure/specs-directory-structure/logical-owner-corpus.md).

## Structure

```
specs/libs/fsharp-crane-core/
├── README.md
├── architecture.md     # the current, as-built library
└── behaviors/          # Gherkin feature files, one folder per capability
    └── convert/
```

## Status

`test:unit` (`dotnet test`) exercises `CraneCore` directly via xUnit tests under
`libs/fsharp-crane-core/tests/unit/Tests/`; no Gherkin runner is wired up for this library yet, so
`specs:behavior:coverage` remains an `echo` placeholder until that lands.

- [Architecture](./architecture.md) — fsharp-crane-core
- [Behaviors](./behaviors/README.md) — fsharp-crane-core
