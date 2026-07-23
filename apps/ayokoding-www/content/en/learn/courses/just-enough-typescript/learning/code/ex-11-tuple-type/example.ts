// Example 11: Tuple Type -- a fixed-length, per-position-typed array.
const p: [number, number] = [1, 2]; // => p is [1, 2] (type: [number, number])
const [x, y] = p; // => destructures the tuple by position
console.log(x, y); // => Output: 1 2
