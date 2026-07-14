// Example 12: Named Tuple -- position labels document intent; arity is still enforced.
const rgb: [r: number, g: number, b: number] = [255, 0, 0]; // => rgb is [255, 0, 0]
const [r, g, b] = rgb; // => labels (r, g, b) show up in editor hovers, not at runtime
console.log(r, g, b); // => Output: 255 0 0
