// Example 64: index.ts -- a barrel that re-exports both siblings from ONE path.
export { addOne } from "./a"; // => re-exports a.ts's addOne, unchanged
export { double } from "./b"; // => re-exports b.ts's double, unchanged
