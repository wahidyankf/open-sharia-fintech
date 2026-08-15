---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 make ownership visible before concurrency. Each file is annotated with its canonical
`co-NN` concept and runs through the shared Cargo manifest. The compile-error lessons show the
minimal safe repair; uncommenting their marked rejected line is an intentional compiler exercise.

Key ideas: moving is a transfer, `&T` observes without moving, `&mut T` is exclusive, a reference
cannot outlive its value, and `Drop` releases resources at scope end.
