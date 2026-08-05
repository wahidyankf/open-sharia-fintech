# Example source map

Every example from `ex-01` through `ex-78` has a colocated runnable .NET project. Its canonical
path is `ex-NN-slug/slug.csproj`, with the documented C# source in `Program.cs` (or `UnitTest1.cs`
for the `dotnet test` example). Run a console example from this directory with:

```sh
dotnet run --project ex-NN-slug/slug.csproj
```

Example `ex-03-dotnet-test-cmd` is an xUnit project, so run it with `dotnet test` instead. Example
`ex-54-nuget-add-package` restores Humanizer before it runs. Example `ex-11-null-analysis-warning`
intentionally emits CS8602 when built; provide a line of input when running it to avoid the nullable
dereference at runtime. The capstone and drills remain separate, full runnable projects.

## Syllabus mapping

- `ex-01` · `dotnet-new-console`
- `ex-02` · `dotnet-run`
- `ex-03` · `dotnet-test-cmd`
- `ex-04` · `top-level-statements`
- `ex-05` · `var-inference`
- `ex-06` · `int-string-bool`
- `ex-07` · `value-type-copy`
- `ex-08` · `reference-type-alias`
- `ex-09` · `nullable-enable`
- `ex-10` · `nullable-annotation`
- `ex-11` · `null-analysis-warning`
- `ex-12` · `null-forgiving`
- `ex-13` · `string-interpolation`
- `ex-14` · `string-methods`
- `ex-15` · `namespace-declare`
- `ex-16` · `using-directive`
- `ex-17` · `class-define`
- `ex-18` · `class-constructor`
- `ex-19` · `class-method`
- `ex-20` · `auto-property`
- `ex-21` · `init-property`
- `ex-22` · `expression-bodied`
- `ex-23` · `enum-define`
- `ex-24` · `array`
- `ex-25` · `list-generic`
- `ex-26` · `dictionary`
- `ex-27` · `interface-define`
- `ex-28` · `interface-implement`
- `ex-29` · `default-interface-member`
- `ex-30` · `inheritance-base`
- `ex-31` · `override-virtual`
- `ex-32` · `record-define`
- `ex-33` · `record-value-equality`
- `ex-34` · `record-with`
- `ex-35` · `record-positional`
- `ex-36` · `struct-value`
- `ex-37` · `struct-vs-class`
- `ex-38` · `generic-method`
- `ex-39` · `generic-class`
- `ex-40` · `generic-constraint`
- `ex-41` · `linq-query-where`
- `ex-42` · `linq-query-select`
- `ex-43` · `linq-method-where`
- `ex-44` · `linq-method-orderby`
- `ex-45` · `linq-chain`
- `ex-46` · `deferred-execution`
- `ex-47` · `immediate-execution`
- `ex-48` · `lambda-expression`
- `ex-49` · `func-delegate`
- `ex-50` · `action-delegate`
- `ex-51` · `lambda-in-linq`
- `ex-52` · `list-of-records`
- `ex-53` · `interface-polymorphism`
- `ex-54` · `nuget-add-package`
- `ex-55` · `switch-expression`
- `ex-56` · `is-pattern`
- `ex-57` · `property-pattern`
- `ex-58` · `tuple-pattern`
- `ex-59` · `try-catch`
- `ex-60` · `catch-specific-exception`
- `ex-61` · `finally-block`
- `ex-62` · `throw-custom`
- `ex-63` · `throw-expression`
- `ex-64` · `async-method`
- `ex-65` · `await-task`
- `ex-66` · `async-return-value`
- `ex-67` · `async-non-blocking`
- `ex-68` · `multiple-await`
- `ex-69` · `task-whenall`
- `ex-70` · `async-exception`
- `ex-71` · `linq-aggregate`
- `ex-72` · `generic-linq-combined`
- `ex-73` · `record-pattern-match`
- `ex-74` · `nullable-linq`
- `ex-75` · `interface-generic`
- `ex-76` · `async-linq-pipeline`
- `ex-77` · `domain-model-slice`
- `ex-78` · `capstone-cli`
