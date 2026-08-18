---
title: "FP-Variant Multi-Language Convention — Examples: FAIL Non-Idiomatic Patterns"
description: Two non-compliant examples — a Clojure tab mechanically simulating an F# DU, and an F# tab suppressing a DU to mirror Clojure's tagged-map approach.
when_to_use: Use when reviewing an FP-variant example and suspecting one tab was mechanically translated from the other rather than written idiomatically.
category: explanation
subcategory: conventions
tags:
  - fp
  - clojure
  - fsharp
  - by-example
  - ayokoding-www
  - tutorial
created: 2026-05-17
---

# Examples: FAIL Non-Idiomatic Patterns

## FAIL: Clojure tab mechanically simulates F# DU

````markdown
{{< tab >}}

```clojure
;; BAD: simulating F# discriminated union with a defrecord hierarchy
(defrecord Draft [])
(defrecord PendingApproval [])
(defrecord Approved [approved-by])
(defrecord Rejected [reason])
(defrecord Closed [])
```

{{< /tab >}}
````

**Why this fails:** `defrecord` used purely to clone an F# DU shape is non-idiomatic Clojure. Idiomatic Clojure represents domain states as maps with a `:status` keyword and uses multimethods or cond for dispatch. The code above forces F#'s closed-type model onto Clojure, which misleads learners about Clojure design style.

## FAIL: F# tab suppresses DU to mirror Clojure map approach

````markdown
{{< tab >}}

```fsharp
// BAD: simulating Clojure tagged maps in F#
let draft = Map.ofList [("tag", box "draft")]
let approved = Map.ofList [("tag", box "approved"); ("approvedBy", box "Alice")]
```

{{< /tab >}}
````

**Why this fails:** Using `Map` to simulate tagged data in F# loses type safety, exhaustiveness checking, and all the benefits of the type system. This forces Clojure's data-orientation philosophy onto F# in a way that is both non-idiomatic and educationally misleading.
