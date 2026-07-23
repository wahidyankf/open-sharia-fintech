// Example 44: Generic Two Params -- <A, B> preserves BOTH argument types in the tuple result.
function pair<A, B>(a: A, b: B): [A, B] {
  // => the return type is a tuple, not a generic array -- each position keeps its own type
  return [a, b];
}

const result = pair(1, "one"); // => result's type is [number, string], not (number | string)[]
console.log(result); // => Output: [ 1, 'one' ]
