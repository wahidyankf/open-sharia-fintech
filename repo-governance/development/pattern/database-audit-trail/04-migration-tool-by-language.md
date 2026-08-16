---
title: "Migration Tool by Language"
description: "Which migration tool each backend app uses to apply the audit columns, and where to find polyglot patterns."
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
when_to_use: "Use when you need to know which migration tool a given backend app uses before writing a migration."
---

# Migration Tool by Language

Each backend uses the idiomatic migration tool for its language and framework ecosystem. All tools must apply the same six audit columns to every table.

| App             | Migration Tool | License |
| --------------- | -------------- | ------- |
| organiclever-be | DbUp           | MIT     |
| ose-be          | DbUp           | MIT     |

For licensing decisions related to Liquibase's FSL-1.1-ALv2 licence (introduced in version 5.0), see [Licensing Decisions](../../../../docs/explanation/software-engineering/licensing/licensing-decisions.md).
