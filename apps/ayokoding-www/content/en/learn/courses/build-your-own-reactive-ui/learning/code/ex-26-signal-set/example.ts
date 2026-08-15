// signal-set: independently runnable, strict TypeScript demonstration.
// => Run with npx tsx example.ts; every assertion is part of the example.

function assert(condition: boolean, message: string): void {
  // => A failed runtime contract must stop the lesson, not merely log a warning.
  if (!condition) throw new Error(message);
  // => PASS: the invariant remains true and execution continues.
}

type Row = Readonly<{ key: string; node: object }>;
// => A row's key describes data identity; node stands in for a mounted DOM node.
const reconcile = (previous: readonly Row[], keys: readonly string[]): readonly Row[] => {
  // => Build lookup once so reordering does not depend on old array positions.
  const byKey = new Map(previous.map((row) => [row.key, row]));
  // => Existing keys map back to their original mounted node objects.
  return keys.map((key) => byKey.get(key) ?? { key, node: {} });
  // => New keys allocate a node; known keys reuse their prior identity.
};
const first = reconcile([], ["a", "b", "c"]);
// => Initial mount creates three independent row nodes.
const reordered = reconcile(first, ["c", "a", "b"]);
// => The next logical order changes, but each item keeps its own key.
assert(reordered[0].node === first[2].node, "key c must move, not recreate");
// => PASS: stable key follows the item across its positional move.
assert(reordered[1].node === first[0].node, "key a must retain identity");
// => This is the behavior positional indexes cannot provide after reordering.
console.log("PASS: signal-set");
// => Output: PASS: signal-set
