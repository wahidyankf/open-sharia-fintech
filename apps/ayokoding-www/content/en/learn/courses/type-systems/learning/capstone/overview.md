---
title: "Capstone: Verified Email"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

The capstone models a verified email as a distinct state rather than a boolean beside a string.
A parser returns Result, and only the Verified constructor is accepted by the send operation. This
is the practical form of making illegal states unrepresentable.

The primary OCaml source is mirrored in Haskell and F# to compare syntax, not to claim the
implementations share identical standard libraries.
