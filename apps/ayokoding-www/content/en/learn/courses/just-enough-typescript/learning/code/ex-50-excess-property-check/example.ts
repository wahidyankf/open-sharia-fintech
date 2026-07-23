// Example 50: Excess Property Check -- only object LITERALS get this stricter check.
type Point2D = { x: number; y: number };

const flat: Point2D = { x: 1, y: 2 }; // => an exact-shape literal -- no extra fields
console.log(flat); // => Output: { x: 1, y: 2 }
