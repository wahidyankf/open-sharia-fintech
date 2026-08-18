---
title: "F# Entity Implementation"
description: "How to map an audited table to an F# EF Core entity, run DbUp migrations at startup, and implement soft-delete in the repository layer."
category: explanation
subcategory: development
tags:
  - database
  - audit-trail
  - soft-delete
  - dbup
  - ef-core
  - migrations
created: 2026-03-09
when_to_use: "Use when implementing the F# entity type, startup migration wiring, or repository soft-delete logic for an audited table."
---

# F# Entity Implementation

## EF Core Entity Type

Map every audited table to an F# record type and configure audit columns explicitly via `IEntityTypeConfiguration`.

```fsharp
// Contexts/Members/Infrastructure/MemberEntity.fs
module Contexts.Members.Infrastructure.MemberEntity

open System
open Microsoft.EntityFrameworkCore
open Microsoft.EntityFrameworkCore.Metadata.Builders

[<CLIMutable>]
type MemberEntity =
    { Id: Guid
      Name: string
      CreatedAt: DateTimeOffset
      CreatedBy: string
      UpdatedAt: DateTimeOffset
      UpdatedBy: string
      DeletedAt: DateTimeOffset option
      DeletedBy: string option }

type MemberEntityConfiguration() =
    interface IEntityTypeConfiguration<MemberEntity> with
        member _.Configure(builder: EntityTypeBuilder<MemberEntity>) =
            builder.ToTable("members") |> ignore
            builder.HasKey(fun m -> m.Id :> obj) |> ignore
            builder.Property(fun m -> m.CreatedBy).HasMaxLength(255).HasDefaultValue("system") |> ignore
            builder.Property(fun m -> m.UpdatedBy).HasMaxLength(255).HasDefaultValue("system") |> ignore
```

## Run Migrations at Startup

Call DbUp in `Program.fs` before the HTTP server starts accepting requests.

```fsharp
// Program.fs (excerpt)
open DbUp

let upgrader =
    DeployChanges
        .To
        .PostgresqlDatabase(connectionString)
        .WithScriptsFromFileSystem("Migrations")
        .LogToConsole()
        .Build()

let result = upgrader.PerformUpgrade()
if not result.Successful then
    failwithf "DbUp migration failed: %s" (result.Error.Message)
```

## Soft-Delete in the Repository Layer

`deleted_at` and `deleted_by` are set explicitly in the repository layer. Never issue a `DELETE` statement on audited tables; always use a soft-delete `UPDATE`.

```fsharp
// Contexts/Members/Infrastructure/EfCoreMemberRepository.fs (excerpt)
member _.SoftDelete(id: Guid, actor: string) =
    task {
        let! member_ =
            dbContext.Members
                .Where(fun m -> m.Id = id && not m.DeletedAt.HasValue)
                .FirstOrDefaultAsync()
        match box member_ with
        | null -> return Error "not found"
        | _ ->
            dbContext.Members.Entry(member_).CurrentValues["DeletedAt"] <- DateTimeOffset.UtcNow
            dbContext.Members.Entry(member_).CurrentValues["DeletedBy"] <- actor
            let! _ = dbContext.SaveChangesAsync()
            return Ok ()
    }
```
