// Kata 1 (after): a list rendered with STABLE id keys keeps per-item state on reorder.
// THE FIX: key = item.id (a stable identity), so the draft follows the ITEM when it moves.

interface Item {
  id: string; // the STABLE key
  label: string;
}

function renderByKey(items: Item[], drafts: Map<string, string>): string[] {
  // THE FIX: key = item.id -> the draft is tied to the ITEM, not the slot
  return items.map((item) => {
    const key = item.id; // => stable identity key
    return `${item.label}="${drafts.get(key) ?? ""}"`; // => draft follows the item
  });
}

const drafts = new Map<string, string>([["a", "typed-in-first"]]); // => draft keyed by item id "a"
const before: Item[] = [
  { id: "a", label: "A" },
  { id: "b", label: "B" },
  { id: "c", label: "C" },
];
const reordered: Item[] = [
  { id: "b", label: "B" },
  { id: "a", label: "A" },
  { id: "c", label: "C" },
];

console.log("before reorder:", renderByKey(before, drafts)); // => A="typed-in-first"
console.log("after reorder: ", renderByKey(reordered, drafts)); // => A="typed-in-first" (draft moved WITH item A)
