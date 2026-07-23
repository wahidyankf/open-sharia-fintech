---
title: "Overview"
weight: 10000000
date: 2026-05-20T00:00:00+07:00
draft: false
description: "Procedural variant — Finite State Machines through three native idioms with canonical literature for each: Go (looplab/fsm + switch dispatch), Rust (typestate with compile-time-enforced transitions), and C (function-pointer table + Miro Samek hierarchical statecharts)"
tags: ["fsm", "finite-state-machine", "tutorial", "by-example", "procedural", "state-patterns", "go", "rust", "c"]
---

**FSM is the architecture topic with the widest paradigm reach on this site.** Three procedural-flavoured languages each have a **canonical native FSM idiom** with first-class published literature — none of which collapse to the OOP "state pattern" or the FP "discriminated union + pure transition function" formulations taught in the sibling tracks.

This is an **in-progress track**. The overview and paradigm framing on this page are stable. Full beginner / intermediate / advanced example content rolls out under the [architecture-procedural-track plan](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## Three Native Idioms

| Language | Idiom                                                             | Mechanism                                                                                                                                    | Error detection                                                     |
| -------- | ----------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------- |
| **Rust** | Typestate                                                         | Each state is a distinct struct type; transitions consume `self` and return a different state type; ownership prevents holding the old state | **Compile-time** — illegal transitions fail to compile              |
| **Go**   | Switch dispatch + [`looplab/fsm`](https://github.com/looplab/fsm) | State as a field (`int` / `string`); transitions via `switch`; library adds event-table configuration + callbacks                            | **Runtime** — invalid transitions return an error                   |
| **C**    | Function-pointer table                                            | 2D array `action[state][event]` of function pointers; each cell is the transition action                                                     | **Runtime** — invalid combinations point at a null or no-op handler |

The Rust typestate idiom is the **strongest compile-time FSM guarantee available in any language taught on this site**. The Go and C idioms are runtime-checked but have the deepest production track record — looplab/fsm has 3.4k stars and active maintenance (v1.0.3, May 2025); the C function-pointer table is the idiom used by the Linux kernel TCP state machine and USB stack at production scale.

## Rust Typestate — Why It Deserves Its Own Track

In the FP formulation (taught in the sibling [in-fp-by-example](/en/learn/software-engineering/software-architecture/finite-state-machine-fsm/in-fp-by-example) track), states are variants of one `enum`:

```fsharp
type PurchaseOrder =
  | Draft of DraftPo
  | AwaitingApproval of AwaitingApprovalPo
  | Approved of ApprovedPo
  | Issued of IssuedPo
```

The transition function returns a new value, but the caller _can_ keep using the old `Draft` — it remains in scope. Tooling and discipline prevent misuse; the type system does not.

In the Rust typestate idiom, each state is a **distinct struct type**:

```rust
struct Draft { /* ... */ }
struct AwaitingApproval { /* ... */ }
struct Approved { /* ... */ }
struct Issued { /* ... */ }

impl Draft {
    pub fn submit(self) -> Result<AwaitingApproval, SubmitError> { /* ... */ }
}
```

The `self` consumption is the critical detail. After `let awaiting = draft.submit()?;` the variable `draft` is **gone** — using it is a compile error. The legal transition graph is enforced by the type system; no runtime check is necessary.

Canonical sources:

- **Ana Hoverbear — [Pretty State Machine Patterns in Rust](https://hoverbear.org/blog/rust-state-machine-pattern/)** — original worked walkthrough showing progression from enum (runtime errors) to typestate (compile errors).
- **Will Crichton — [Type-Driven API Design in Rust](https://willcrichton.net/rust-api-type-patterns/typestate.html)** — Stanford academic treatment of typestate as Rust API design discipline.

## Go's Native FSM — looplab/fsm + Switch Dispatch

Go's canonical FSM idiom is **state as a field** with `switch` dispatch on `(currentState, event)`. The most-cited library is [looplab/fsm](https://github.com/looplab/fsm) which lifts the switch table into a declarative event configuration:

```go
fsm := fsm.NewFSM(
    "draft",
    fsm.Events{
        {Name: "submit", Src: []string{"draft"}, Dst: "awaiting_approval"},
        {Name: "approve", Src: []string{"awaiting_approval"}, Dst: "approved"},
        {Name: "issue", Src: []string{"approved"}, Dst: "issued"},
        {Name: "cancel", Src: []string{"draft", "awaiting_approval", "approved"}, Dst: "cancelled"},
    },
    fsm.Callbacks{
        "enter_awaiting_approval": func(_ context.Context, e *fsm.Event) { /* notify approver */ },
    },
)
```

Stats: 3.4k stars, Apache 2.0, v1.0.3 (May 2025), active maintenance. Used in production across the Go ecosystem for workflow engines, payment state machines, and order lifecycles.

## C's Native FSM — Function-Pointer Table

The C idiom is a 2D array `action[state][event]` of function pointers; each cell is the transition action. State is an enum index. Miro Samek's [_Practical UML Statecharts in C/C++_](https://www.routledge.com/Practical-UML-Statecharts-in-CC-Event-Driven-Programming-for-Embedded-Systems/Samek/p/book/9780750687065) (CRC Press, 2nd ed. 2008) is the authoritative book-length treatment, covering hierarchical state machines via the QP/C active-object framework. Published source at [state-machine.com/psicc2](https://www.state-machine.com/psicc2).

Real-world examples at production scale:

- **Linux kernel TCP state machine** (`net/ipv4/tcp.c`) — TCP socket lifecycle via state-and-event dispatch.
- **Linux kernel USB stack** — device enumeration and connection state.
- **Embedded RTOS code** — bare-metal and real-time systems use Samek-style hierarchical statecharts extensively.

## What This Tutorial Will Cover

**Rust typestate examples** — moving `self` through the procurement state machine (Draft → AwaitingApproval → Approved → Issued → Received → Invoiced → Paid), with cancel off-ramps from any pre-paid state, guard conditions via constructor functions on the next-state type, hierarchical states via composition of typestate structs.

**Go looplab/fsm examples** — declarative event configuration for the same procurement state machine, callback hooks for entry/exit actions, integration with the Go `procurement-platform-be` package layout, runtime validation, persistence to JSON for FSM snapshot/resume.

**C function-pointer table examples** — Samek-style hierarchical state machine for a simpler subset (e.g., supplier lifecycle), demonstrating the function-pointer dispatch idiom and QP/C event-driven event-driven active-object framework.

## Running Domain

Same `procurement-platform-be` Procure-to-Pay state machines (`PurchaseOrder`, `Invoice`, `Supplier`, `Payment`, `MurabahaContract`) as the OOP and FP tracks.

## Sibling Tutorials

- [FSM By Example in OOP](/en/learn/software-engineering/software-architecture/finite-state-machine-fsm/in-oop-by-example/overview) — Java (canonical), Kotlin, C#, TypeScript with XState.
- [FSM By Example in FP](/en/learn/software-engineering/software-architecture/finite-state-machine-fsm/in-fp-by-example/overview) — F# (canonical), Clojure, TypeScript, Haskell with discriminated unions and pure transition functions.

## Rollout Plan

Full beginner / intermediate / advanced example content authoring tracks under [`plans/in-progress/architecture-procedural-track/`](https://github.com/wahidyankf/ose-public/tree/main/plans/in-progress/architecture-procedural-track).

## Structure of Each Example (Planned)

1. **Brief Explanation** — what FSM concept the example demonstrates (2-3 sentences).
2. **State Diagram** — Mermaid `stateDiagram-v2` with accessible color palette.
3. **Heavily Annotated Code** — parallel tabs: Rust (typestate canonical for compile-time-checked FSMs), Go (looplab/fsm canonical for runtime-checked workflow FSMs), C (Samek canonical for embedded systems where applicable). `// =>` annotations at 1.0–2.25 comment lines per code line per tab.
4. **Key Takeaway** — the core FSM principle (1-2 sentences).
5. **Why It Matters** — design rationale and consequences (50-100 words).
