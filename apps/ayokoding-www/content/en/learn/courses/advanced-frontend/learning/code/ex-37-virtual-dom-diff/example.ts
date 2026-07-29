// Example 37: Diffing Two Virtual Trees Patches Only the Delta. (co-21)
//
// A virtual DOM is a plain-object description of the real DOM. Re-rendering produces a NEW tree;
// the diff finds the MINIMAL set of changes (the delta) between old and new, and only those are
// applied to the real DOM. This is the O(n) heuristic at the heart of React's reconciliation.

// A virtual node: a tag, some props, and children (text or more vnodes).
interface VNode {
  // => the smallest tree description needed to show a diff
  tag: string; // => the element type
  props: Record<string, string>; // => attributes (class, etc.)
  children: Array<VNode | string>; // => nested nodes or text leaves
}

// Each patch the diff would apply to the real DOM.
type Patch =
  | { kind: "text"; oldText: string; newText: string } // => a text leaf changed
  | { kind: "prop"; name: string; oldVal: string; newVal: string }; // => a prop changed
// => a real reconciler also handles insert/remove/move; these two suffice to show "only the delta"

// diff compares old vs new vnode and returns ONLY the patches that differ.
function diff(oldNode: VNode, newNode: VNode): Patch[] {
  // => co-21: same tag => reuse the node, collect only the changed props/text
  const patches: Patch[] = [];
  for (const key of Object.keys(newNode.props)) {
    // => compare each prop; record only the ones that actually changed
    const oldVal = oldNode.props[key] ?? ""; // => treat missing as empty
    const newVal = newNode.props[key];
    if (oldVal !== newVal) patches.push({ kind: "prop", name: key, oldVal, newVal }); // => a delta
  }
  for (let i = 0; i < newNode.children.length; i++) {
    // => compare children pairwise; record only changed text leaves
    const o = oldNode.children[i];
    const n = newNode.children[i];
    if (typeof o === "string" && typeof n === "string" && o !== n) {
      patches.push({ kind: "text", oldText: o, newText: n }); // => only the changed text
    }
  }
  return patches; // => the minimal delta
}

// Only the class prop and the title text changed between these two renders.
const oldTree: VNode = { tag: "h1", props: { class: "old", id: "h" }, children: ["Hello"] };
const newTree: VNode = { tag: "h1", props: { class: "new", id: "h" }, children: ["World"] };

const patches = diff(oldTree, newTree); // => only 2 patches, not a full rebuild

console.log("patches:", JSON.stringify(patches)); // => Output: patches: [{"kind":"prop",...},{"kind":"text",...}]
console.log("patch count:", patches.length); // => Output: patch count: 2
