// Example 38: A Same Type Element Reuses Its DOM Node. (co-20, co-21)
//
// During reconciliation, when the element at a given position is the SAME type in both renders
// (e.g. <div> -> <div>), React REUSES the existing DOM node and updates only its changed props/
// children. The node's identity is preserved -- no teardown, no recreation.

// A real DOM node we can ask "is this the SAME object as before?"
interface DomEl {
  // => identity is what "reuse" means: the very same object, mutated in place
  id: number; // => a unique identity we can compare across renders
  tag: string; // => the element type
  className: string; // => a mutable prop
}

let nextId = 1; // => a monotonic id so we can detect whether a node was reused or recreated

// reconcileSameType updates the EXISTING node when the type matches; returns whether it was reused.
function reconcileSameType(existing: DomEl, newTag: string, newClass: string): { reused: boolean; node: DomEl } {
  // => co-20/co-21: same type => reuse; the node keeps its id, only its props change
  if (existing.tag === newTag) {
    existing.className = newClass; // => mutate in place -- the node is reused
    return { reused: true, node: existing }; // => SAME id as before
  }
  return { reused: false, node: { id: nextId++, tag: newTag, className: newClass } }; // => (Example 39's case)
}

const before: DomEl = { id: nextId++, tag: "div", className: "old" }; // => the existing node
const after = reconcileSameType(before, "div", "new"); // => same type -> reuse
// => `after.node` IS `before` (same id, same object) -- only className changed

console.log("reused same node:", after.reused); // => Output: reused same node: true
console.log("same identity (id):", before.id === after.node.id); // => Output: same identity (id): true
