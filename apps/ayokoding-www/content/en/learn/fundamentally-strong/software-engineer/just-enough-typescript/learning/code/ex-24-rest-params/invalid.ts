// Example 24 (invalid): a string argument does not fit the number[] rest parameter.
function sum(...nums: number[]): number {
  return nums.reduce((total, n) => total + n, 0);
}

console.log(sum(1, "two", 3)); // => TYPE ERROR: string is not assignable to number
