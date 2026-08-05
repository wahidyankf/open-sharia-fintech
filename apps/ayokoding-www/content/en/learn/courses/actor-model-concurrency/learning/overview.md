---
title: "Overview"
date: 2026-08-04T00:00:00+07:00
draft: false
weight: 1
---

Actor-model concurrency organizes mutable state around isolated processes that exchange messages.
This course uses Elixir to build from a process mailbox to monitors, GenServers, registries, and
supervision trees.

## Prerequisites

- Complete [Just Enough Elixir](../../just-enough-elixir/learning/overview.md) for pattern matching,
  functions, processes, and the `mix` workflow.
- Complete the shared [Concurrency and Parallelism](../../concurrency-and-parallelism/learning/overview.md)
  course for the vocabulary of safety, liveness, back-pressure, and cancellation.

## What you will build

The learning track contains executable process and GenServer examples. The capstone packages a small
supervised service with its state, client API, and tests separated by process boundaries.

## Scope boundary

This course owns actor isolation, message protocols, supervision, and OTP-style service structure. It
does not replace the Elixir primer, teach CSP channels, or cover distributed-cluster operations.
