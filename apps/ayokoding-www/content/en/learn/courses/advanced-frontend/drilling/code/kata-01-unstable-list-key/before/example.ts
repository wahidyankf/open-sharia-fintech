// Kata 1 (before): a list rendered with INDEX keys loses per-item state on reorder.
// THE BUG: the key is the array INDEX, so a per-item draft (here, typed text) attaches to a
// POSITION, not to an ITEM. Reordering moves the items but the drafts stay put -> wrong item
// shows the draft.

interface Item {
  id: string; // a stable identity the key SHOULD use
  label: string; // the visible text
}

// Render the list, keying the per-item draft by... the INDEX (the bug).
function renderByKey(items: Item[], drafts: Map<string, string>): string[] {
  // THE BUG: key = String(index) -> the draft is tied to the slot, not the item
  return items.map((item, index) => {
    const key = String(index); // => position key, NOT a stable identity
    return `${item.label}="${drafts.get(key) ?? ""}"`; // => draft follows the slot
  });
}

const drafts = new Map<string, string>([["0", "typed-in-first"]]); // => draft at slot 0
const before: Item[] = [
  { id: "a", label: "A" },
  { id: "b", label: "B" },
  { id: "c", label: "C" },
];

// Reorder: move B to the front. With index keys, slot 0's draft now attaches to B, not A.
const reordered: Item[] = [
  { id: "b", label: "B" },
  { id: "a", label: "A" },
  { id: "c", label: "C" },
];

console.log("before reorder:", renderByKey(before, drafts)); // => A="typed-in-first"
console.log("after reorder: ", renderByKey(reordered, drafts)); // => BUG: B="typed-in-first" (draft stuck to slot)
