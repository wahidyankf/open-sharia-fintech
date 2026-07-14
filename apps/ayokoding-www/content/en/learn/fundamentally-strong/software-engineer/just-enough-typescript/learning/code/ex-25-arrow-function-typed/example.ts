// Example 25: Arrow Function Typed -- arrow functions carry the same annotations as `function`.
const double = (n: number): number => n * 2; // => n: number in, number out

console.log(double(21)); // => Output: 42
