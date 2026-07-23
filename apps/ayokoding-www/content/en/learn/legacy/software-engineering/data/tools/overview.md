---
title: Overview
weight: 100000
date: 2025-12-23T00:00:00+07:00
draft: false
description: Master database migration and data-access tools across languages — schema versioning, ORMs, and type-safe query libraries
---

Data tools manage how applications evolve and access their databases. This section covers two complementary families: **schema migration tools** that version-control your database structure over time, and **data-access libraries** (ORMs and query DSLs) that bridge your application's object or data model and relational databases. Each tool has a By Example tutorial in its language's idiom.

## Schema Migration Tools

Migration tools apply ordered, reversible changes to your database schema so it evolves safely alongside your code:

- **[Liquibase](/en/learn/software-engineering/data/tools/java-liquibase)** (Java) - Changelog-based migrations in SQL, XML, YAML, or JSON with rollback support.
- **[Flyway](/en/learn/software-engineering/data/tools/kotlin-flyway)** (Kotlin) - Version-based, SQL-first migrations with a simple, convention-driven workflow.
- **[Alembic](/en/learn/software-engineering/data/tools/python-alembic)** (Python) - SQLAlchemy's migration engine with autogeneration and branching.
- **[Goose](/en/learn/software-engineering/data/tools/golang-goose)** (Go) - Lightweight migrations in SQL or Go functions.
- **[Migratus](/en/learn/software-engineering/data/tools/clojure-migratus)** (Clojure) - Data-driven SQL migrations for the JVM.
- **[DbUp](/en/learn/software-engineering/data/tools/fsharp-dbup)** (F#) - Script-based .NET migrations that track applied changes.

## Data Access & ORMs

Data-access tools map between application code and relational data:

- **[Spring Data JPA](/en/learn/software-engineering/data/tools/spring-data-jpa)** (Java) - JPA/Hibernate persistence with the repository pattern and query-method generation.
- **[EF Core](/en/learn/software-engineering/data/tools/csharp-ef-core)** (C#) - Entity Framework Core ORM with LINQ queries and built-in migrations.
- **[Ecto](/en/learn/software-engineering/data/tools/elixir-ecto)** (Elixir) - Functional database wrapper with composable queries and changeset validation.
- **[SQLx](/en/learn/software-engineering/data/tools/rust-sqlx)** (Rust) - Async, compile-time-checked SQL without a heavyweight ORM.
- **[Effect SQL](/en/learn/software-engineering/data/tools/typescript-effect-sql)** (TypeScript) - Type-safe SQL access built on the Effect runtime.

## Learning Approach

Each tool provides a **By Example** tutorial with practical, annotated, runnable code:

- **Beginner** - Core concepts, basic CRUD or first migrations, fundamentals
- **Intermediate** - Complex queries, relationships, transactions, environments
- **Advanced** - Performance optimization, custom queries, advanced patterns

## Choosing Your Tool

- **Pick by ecosystem first** - use the migration or data-access tool idiomatic to your language and framework.
- **Migration vs. ORM** - migration tools manage schema _structure_ over time; ORMs and query libraries manage _runtime data access_. Most production systems use both: a migration tool to evolve the schema and a data-access library to read and write rows.
- **SQL knowledge helps** - all of these assume basic SQL. Complete the [SQL](/en/learn/software-engineering/data/databases/sql) tutorial first if you're new to relational databases.
