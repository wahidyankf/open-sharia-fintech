// Example 10: readonly Array -- readonly T[] removes every mutating method at compile time.
const xs: readonly number[] = [1, 2, 3]; // => xs is [1, 2, 3] (type: readonly number[])
console.log(xs[0]); // => reading by index is still allowed -- Output: 1
console.log(xs.length); // => Output: 3
