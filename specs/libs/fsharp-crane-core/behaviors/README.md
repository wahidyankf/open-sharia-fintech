# Behaviors — fsharp-crane-core

Gherkin feature files for [fsharp-crane-core](../../../../libs/fsharp-crane-core/project.json),
one folder per capability.

```
specs/libs/fsharp-crane-core/behaviors/
└── convert/
    └── pdf-to-markdown-routing.feature
```

## Consumption

No Gherkin runner consumes these scenarios yet — `fsharp-crane-core` is exercised via xUnit tests
(`dotnet test`) under `libs/fsharp-crane-core/tests/unit/Tests/`. See the corpus
[README.md](../README.md#status).
