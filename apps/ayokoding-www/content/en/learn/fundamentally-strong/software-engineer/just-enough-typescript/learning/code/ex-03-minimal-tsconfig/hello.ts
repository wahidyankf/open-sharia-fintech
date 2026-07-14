// Example 3: Minimal tsconfig -- this file relies on the sibling tsconfig.json for its
// compiler options (target: ES2022, module: ESNext, strict: true).
const ready: boolean = true; // => ready is true (type: boolean)
console.log(ready); // => logs ready to stdout
// => Output: true
