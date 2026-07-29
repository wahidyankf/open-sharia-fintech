// Example 39: A Different Type Element Rebuilds the Subtree. (co-21)
//
// When the element at a position CHANGES type between renders (e.g. <div> -> <span>), React treats
// it as a different element: it TEARS DOWN the old subtree (and its state) and builds a fresh one.
// This is why toggling between different component types resets state.

// Each DOM node has an identity and a type; a type change means a full rebuild.
interface DomEl {
  // => id lets us prove the old node was destroyed, not reused
  id: number; // => identity
  tag: string; // => the type that, if changed, triggers a rebuild
  state: string; // => per-node state that is LOST on rebuild
}

let nextId = 1; // => monotonic ids distinguish reused nodes from freshly-built ones

// reconcileDifferentType rebuilds when the type changes; reuses when it does not.
function reconcile(existing: DomEl, newTag: string): { rebuilt: boolean; node: DomEl; oldId: number } {
  // => co-21: different type => destroy the old subtree (state lost) and build a new node
  if (existing.tag !== newTag) {
    const fresh: DomEl = { id: nextId++, tag: newTag, state: "" }; // => a NEW node, EMPTY state
    return { rebuilt: true, node: fresh, oldId: existing.id }; // => old node torn down
  }
  return { rebuilt: false, node: existing, oldId: existing.id }; // => same type -> reuse (Example 38)
}

const before: DomEl = { id: nextId++, tag: "div", state: "user-typed-text" }; // => old node with state
const result = reconcile(before, "span"); // => div -> span: DIFFERENT type -> rebuild

console.log("rebuilt subtree:", result.rebuilt); // => Output: rebuilt subtree: true
console.log("old id destroyed:", result.oldId, "| new id:", result.node.id); // => different ids
console.log("state after rebuild (lost):", JSON.stringify(result.node.state)); // => Output: state after rebuild (lost): ""
