---
title: "Capstone: Hygienic Unless"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

The capstone combines recursive list processing with a Scheme syntax-rules control form and a
Clojure defmacro sidebar. Run main.rkt with Racket and sidebar.clj with the Clojure CLI.

## Acceptance checks

- The recursive function processes a list through a higher-order map.
- The unless macro adds control syntax without evaluating its protected form when the condition holds.
- The Clojure macro mirrors the behavior and uses syntax quote with an auto-gensym binding.
- Inspect an expansion in the local macro stepper or REPL before treating a macro as trusted.
