---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

## Prerequisites

- [Advanced Frontend](../../advanced-frontend/learning/overview.md) for DOM rendering, reconciliation, and framework-consumer context.
- TypeScript strict mode, discriminated unions, generics, DOM APIs, and browser events. No UI framework is used: the goal is to inspect the runtime mechanisms directly.

## Why this exists -- the big idea

A reactive UI makes the rendered view follow state. This course builds that guarantee twice: first by reconciling typed virtual trees, then by tracking a fine-grained signal graph, so you can see exactly when each approach does work.

## Concepts

### co-01 · view-as-function-of-state

view-as-function-of-state is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-02 · hyperscript

hyperscript is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-03 · jsx-to-h

jsx-to-h is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-04 · virtual-node-tree

virtual-node-tree is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-05 · mount-render

mount-render is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-06 · diff-algorithm

diff-algorithm is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-07 · patch-apply

patch-apply is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-08 · reconciliation-heuristic

reconciliation-heuristic is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-09 · same-type-reuse

same-type-reuse is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-10 · different-type-rebuild

different-type-rebuild is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-11 · keys-list-diffing

keys-list-diffing is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-12 · keys-identity-bug

keys-identity-bug is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-13 · signal-primitive

signal-primitive is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-14 · computed

computed is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-15 · effect

effect is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-16 · automatic-dependency-tracking

automatic-dependency-tracking is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-17 · reactive-graph

reactive-graph is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-18 · observer-pattern

observer-pattern is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-19 · fine-grained-update

fine-grained-update is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-20 · component-model

component-model is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-21 · state-hook

state-hook is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-22 · hooks-call-order

hooks-call-order is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-23 · effect-hook

effect-hook is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-24 · event-delegation

event-delegation is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-25 · batching-scheduling

batching-scheduling is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-26 · proxy-reactivity

proxy-reactivity is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-27 · compiled-reactivity

compiled-reactivity is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-28 · memoization

memoization is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-29 · template-literal-dom

template-literal-dom is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-30 · reconciler-renderer-split

reconciler-renderer-split is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-31 · diamond-problem

diamond-problem is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

### co-32 · disposal-cleanup

disposal-cleanup is a concrete reactive-runtime contract, taught before the examples that exercise it.

**Why it matters**: Correct implementations preserve this contract when state changes, work is scheduled, or the DOM is reconciled. The worked examples make the contract executable rather than leaving it as framework vocabulary.

## How to run examples

Every source artifact is strict TypeScript and contains no `any`. From its directory, run `npx tsx example.ts`; each reports a PASS line or throws on a failed invariant.

## Examples by Level

### Beginner (Examples 1–26)

- [Example 1: H Function](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-1-h-function)
- [Example 2: H Nested](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-2-h-nested)
- [Example 3: VNode Shape](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-3-vnode-shape)
- [Example 4: JSX Desugar](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-4-jsx-desugar)
- [Example 5: Text VNode](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-5-text-vnode)
- [Example 6: Mount Element](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-6-mount-element)
- [Example 7: Mount Props](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-7-mount-props)
- [Example 8: Mount Children](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-8-mount-children)
- [Example 9: Mount Text](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-9-mount-text)
- [Example 10: View As Function](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-10-view-as-function)
- [Example 11: Rerender Naive](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-11-rerender-naive)
- [Example 12: Diff Text Change](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-12-diff-text-change)
- [Example 13: Patch Text](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-13-patch-text)
- [Example 14: Diff Prop Change](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-14-diff-prop-change)
- [Example 15: Patch Prop](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-15-patch-prop)
- [Example 16: Diff Add Child](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-16-diff-add-child)
- [Example 17: Patch Add Child](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-17-patch-add-child)
- [Example 18: Diff Remove Child](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-18-diff-remove-child)
- [Example 19: Patch Remove Child](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-19-patch-remove-child)
- [Example 20: Same Type Reuse](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-20-same-type-reuse)
- [Example 21: Different Type Replace](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-21-different-type-replace)
- [Example 22: Node Identity Preserved](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-22-node-identity-preserved)
- [Example 23: Event Listener Bind](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-23-event-listener-bind)
- [Example 24: Event Update](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-24-event-update)
- [Example 25: Signal Value](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-25-signal-value)
- [Example 26: Signal Set](/en/learn/courses/build-your-own-reactive-ui/learning/beginner#example-26-signal-set)

### Intermediate (Examples 27–54)

- [Example 27: Keyed List Diff](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-27-keyed-list-diff)
- [Example 28: Keyed Reorder Moves](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-28-keyed-reorder-moves)
- [Example 29: Unkeyed List Bug](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-29-unkeyed-list-bug)
- [Example 30: Unstable Key Loses State](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-30-unstable-key-loses-state)
- [Example 31: Keyed Insert](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-31-keyed-insert)
- [Example 32: Keyed Remove](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-32-keyed-remove)
- [Example 33: Signal Effect](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-33-signal-effect)
- [Example 34: Effect Dependency Track](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-34-effect-dependency-track)
- [Example 35: Computed Derive](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-35-computed-derive)
- [Example 36: Computed Lazy](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-36-computed-lazy)
- [Example 37: Computed Cache](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-37-computed-cache)
- [Example 38: Reactive Graph Build](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-38-reactive-graph-build)
- [Example 39: Fine Grained Update](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-39-fine-grained-update)
- [Example 40: Observer Subscribe](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-40-observer-subscribe)
- [Example 41: Observer Unsubscribe](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-41-observer-unsubscribe)
- [Example 42: Effect Cleanup](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-42-effect-cleanup)
- [Example 43: Dispose Effect](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-43-dispose-effect)
- [Example 44: Dispose Avoids Leak](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-44-dispose-avoids-leak)
- [Example 45: Component Function](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-45-component-function)
- [Example 46: Component Props](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-46-component-props)
- [Example 47: useState Closure](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-47-usestate-closure)
- [Example 48: useState Rerender](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-48-usestate-rerender)
- [Example 49: Hooks Call Order](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-49-hooks-call-order)
- [Example 50: Hooks Conditional Bug](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-50-hooks-conditional-bug)
- [Example 51: useEffect After Render](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-51-useeffect-after-render)
- [Example 52: useEffect Deps](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-52-useeffect-deps)
- [Example 53: Memoize Computed](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-53-memoize-computed)
- [Example 54: Signal Vs VDOM Update](/en/learn/courses/build-your-own-reactive-ui/learning/intermediate#example-54-signal-vs-vdom-update)

### Advanced (Examples 55–80)

- [Example 55: Batching Multiple Sets](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-55-batching-multiple-sets)
- [Example 56: Microtask Schedule](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-56-microtask-schedule)
- [Example 57: requestAnimationFrame Schedule](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-57-raf-schedule)
- [Example 58: Proxy Reactive](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-58-proxy-reactive)
- [Example 59: Proxy Track](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-59-proxy-track)
- [Example 60: Proxy Trigger](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-60-proxy-trigger)
- [Example 61: Ref Getter Setter](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-61-ref-getter-setter)
- [Example 62: Compiled Updates](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-62-compiled-updates)
- [Example 63: Compiled Vs VDOM](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-63-compiled-vs-vdom)
- [Example 64: Template Literal Html](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-64-template-literal-html)
- [Example 65: Template Static Dynamic](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-65-template-static-dynamic)
- [Example 66: Template Update Holes](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-66-template-update-holes)
- [Example 67: Reconciler Host Config](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-67-reconciler-host-config)
- [Example 68: Custom Renderer](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-68-custom-renderer)
- [Example 69: Fiber Unit Of Work](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-69-fiber-unit-of-work)
- [Example 70: Diamond Problem](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-70-diamond-problem)
- [Example 71: Diamond Glitch](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-71-diamond-glitch)
- [Example 72: Topological Order](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-72-topological-order)
- [Example 73: Diamond Single Recompute](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-73-diamond-single-recompute)
- [Example 74: Cleanup On Unmount](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-74-cleanup-on-unmount)
- [Example 75: Effect Scope Dispose](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-75-effect-scope-dispose)
- [Example 76: Nested Effects](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-76-nested-effects)
- [Example 77: Signal Batch Consistency](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-77-signal-batch-consistency)
- [Example 78: Event Delegation Root](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-78-event-delegation-root)
- [Example 79: View Function Full](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-79-view-function-full)
- [Example 80: Reactive UI Capstone](/en/learn/courses/build-your-own-reactive-ui/learning/advanced#example-80-reactive-ui-capstone)
