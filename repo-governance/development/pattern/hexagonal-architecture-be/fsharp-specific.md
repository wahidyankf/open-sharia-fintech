---
description: "F#-specific idioms for outbound ports, dependency injection, and mapping domain errors to HTTP responses at the API boundary."
when_to_use: "Use when implementing an F# outbound port interface, wiring DI in Program.fs, or mapping a domain error to an HTTP response."
---

# F#-Specific

## Interfaces as Ports

Outbound ports are F# `interface` definitions in the application layer. Infrastructure modules provide
concrete implementations that depend on EF Core or other infrastructure concerns.

```fsharp
// Contexts/Tasks/Application/Ports.fs  — outbound port (application layer)
module Contexts.Tasks.Application.Ports

open Contexts.Tasks.Domain

type ITaskRepository =
    abstract member FindById : TaskId -> Async<Task option>
    abstract member Save : Task -> Async<unit>
```

## Dependency Injection via ASP.NET 10

Application services receive port interfaces through ASP.NET 10 constructor injection. Infrastructure
implementations are registered in `Program.fs` and never referenced directly by application or domain
modules.

```fsharp
// Program.fs  — wire infrastructure implementations to application ports
builder.Services.AddScoped<ITaskRepository, EfCoreTaskRepository>()
```

## Error Mapping at the API Boundary

Domain errors must not contain HTTP status codes. The `Api/Http/` layer owns the translation to
Giraffe `HttpHandler` responses.

```fsharp
// Contexts/Tasks/Domain/Errors.fs  — domain errors (no HTTP types)
module Contexts.Tasks.Domain.Errors

type DomainError =
    | NotFound of TaskId
    | AlreadyCompleted

// Contexts/Tasks/Api/Http/Errors.fs  — translation at API boundary
module Contexts.Tasks.Api.Http.Errors

open Giraffe
open Contexts.Tasks.Domain.Errors

let toHttpHandler (error: DomainError) : HttpHandler =
    match error with
    | NotFound taskId -> RequestErrors.notFound (text (sprintf "task not found: %A" taskId))
    | AlreadyCompleted -> RequestErrors.conflict (text "task is already completed")
```
