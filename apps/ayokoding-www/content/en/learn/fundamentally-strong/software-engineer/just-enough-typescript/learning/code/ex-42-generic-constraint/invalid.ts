// Example 42 (invalid): a plain number has no .length property, so it fails the constraint.
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(longest(1, 2)); // => TYPE ERROR: number does not satisfy { length: number }
