---
title: "Capstone: Concurrent JSON Status Check"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build the small status checker in `code/main.go`: a struct implements `Checker`, `run` returns error
values rather than exiting, and one goroutine hands its result over a typed channel. Run `go test` from
`learning/capstone/code/`, then run `go run main.go`. This proves package structure, methods,
interfaces, explicit errors, a single goroutine/channel hand-off, and an idiomatic test.
