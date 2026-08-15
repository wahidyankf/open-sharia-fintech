---
title: "Overview"
date: 2026-08-16T00:00:00+07:00
draft: false
weight: 1
---

## Why this exists

Configuration, declared extension points, and core customization have different ownership, compatibility, and upgrade costs. Systems builders must record the boundary and migration consequence of each choice.

## Silent-failure check

### What still balances while being wrong

An extension can work today while directly mutating a core record another upgrade owns. The observable signal is a missing compatibility contract, migration path, or decision owner.
