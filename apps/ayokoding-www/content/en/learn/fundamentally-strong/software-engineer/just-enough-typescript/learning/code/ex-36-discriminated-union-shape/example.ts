// Example 36: Discriminated Union Shape -- a shared literal "kind" field tags each variant.
type Shape =
  | { kind: "circle"; r: number } // => the "circle" variant carries a radius
  | { kind: "square"; s: number }; // => the "square" variant carries a side length

const c: Shape = { kind: "circle", r: 2 }; // => matches the first variant exactly
const s: Shape = { kind: "square", s: 3 }; // => matches the second variant exactly
console.log(c, s); // => Output: { kind: 'circle', r: 2 } { kind: 'square', s: 3 }
