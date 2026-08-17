# fsharp-crane-core Specs

Gherkin behavioral specifications for
[fsharp-crane-core](../../../libs/fsharp-crane-core/project.json), the shared F# domain/logic core
for PDF-to-Markdown conversion and verification.

## Purpose

These specs define the **observable behavior** of the `CraneCore` domain: given a PDF, whether the
conversion walk-skeleton picks the text-extraction or OCR path, and what a resulting `Finding`
looks like.

## Structure

```
specs/libs/fsharp-crane-core/
├── README.md
├── product/               # C4 L1 product framing
├── system-context/        # C4 L1 actors and consumers
├── containers/            # C4 L2 deployable units
├── components/            # C4 L3 component catalogue
└── behavior/
    └── gherkin/           # Gherkin feature files
        └── convert/
```

## Status

`test:unit` (`dotnet test`) exercises `CraneCore` directly via xUnit tests under
`tests/unit/Tests/`; no Cucumber/Gherkin runner is wired up for this crate yet —
`specs:behavior:coverage` is an `echo` placeholder until that lands.

- [Behavior — fsharp-crane-core](./behavior/README.md)
- [Components — fsharp-crane-core](./components/README.md)
- [Containers — fsharp-crane-core](./containers/README.md)
- [Product — fsharp-crane-core](./product/README.md)
- [System Context — fsharp-crane-core](./system-context/README.md)
