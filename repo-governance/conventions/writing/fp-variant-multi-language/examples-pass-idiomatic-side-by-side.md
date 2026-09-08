---
description: A full compliant worked example — discriminated union with pattern matching in F# versus a multimethod in Clojure — with cross-paradigm annotations.
when_to_use: Use as a template when writing a new compliant FP-variant example, or to see what a passing S1-S6 example looks like end to end.
---

# Examples: PASS Idiomatic F# and Clojure Side-by-Side

## PASS: Idiomatic F# and Clojure side-by-side — discriminated union vs. multimethod

This example teaches domain-state dispatch. F# uses a discriminated union with pattern matching (its native mechanism). Clojure uses a multimethod (its native mechanism). Each is explained with a cross-paradigm annotation.

````markdown
{{< tabs items="F#,Clojure" >}}

{{< tab >}}

```fsharp
// Domain state for a purchase requisition lifecycle
// [Clojure: multimethod dispatch on :status key — open extension without exhaustiveness]
type RequisitionStatus =
    // => Five variants cover the full procurement lifecycle
    | Draft                          // => Initial state after creation
    | PendingApproval                // => Submitted, awaiting manager sign-off
    | Approved of approvedBy: string // => Carries approver identity on transition
    | Rejected of reason: string     // => Carries rejection reason for audit trail
    | Closed                         // => Terminal state; no further transitions

// Pattern match is exhaustive — compiler rejects missing cases
let describeStatus status =
    match status with
    | Draft           -> "awaiting submission"        // => Human-readable label
    | PendingApproval -> "pending manager approval"
    | Approved name   -> $"approved by {name}"        // => Interpolates approver name
    | Rejected reason -> $"rejected: {reason}"
    | Closed          -> "closed"
```

{{< /tab >}}

{{< tab >}}

```clojure
;; Domain state for a purchase requisition lifecycle
;; [F#: discriminated union — compiler-enforced exhaustiveness; missing cases are compile errors]
(defmulti describe-status
  ;; Dispatch on the :status key of the requisition map
  :status)
;; => defmulti defines the dispatch function; defmethod adds each variant

(defmethod describe-status :draft [_]
  "awaiting submission")
;; => _ ignores the full map; only the dispatch value matters here

(defmethod describe-status :pending-approval [_]
  "pending manager approval")

(defmethod describe-status :approved [{:keys [approved-by]}]
  ;; Destructure the map to extract the approver identity
  (str "approved by " approved-by))
;; => approved-by comes from the map, not a tagged payload position

(defmethod describe-status :rejected [{:keys [reason]}]
  (str "rejected: " reason))

(defmethod describe-status :closed [_]
  "closed")
;; => Clojure multimethods are open: a new :status variant requires only a new defmethod
;; => F# DUs are closed: adding a variant requires updating all match sites
```

{{< /tab >}}

{{< /tabs >}}
````

**Why this is compliant:**

- F# uses DU + pattern matching — native, exhaustive, compile-time safe.
- Clojure uses defmulti/defmethod — native open dispatch, REPL-friendly, data-oriented.
- Each tab has a cross-paradigm annotation noting the key trade-off.
- Both tabs meet the 1.0–2.25 comment-to-code ratio independently.
