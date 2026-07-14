// Example 27 (invalid): proves n really is inferred as number, not string or any.
const nums: number[] = [1, 2, 3];

const shouty = nums.map((n) => n.toUpperCase()); // => TYPE ERROR: number has no toUpperCase
console.log(shouty);
