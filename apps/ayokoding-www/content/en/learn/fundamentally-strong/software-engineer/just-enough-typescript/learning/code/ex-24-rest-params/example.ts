// Example 24: Rest Params -- ...nums collects every remaining argument into number[].
function sum(...nums: number[]): number {
  // => nums is a typed array of every argument passed after none required before it
  return nums.reduce((total, n) => total + n, 0); // => folds the array into one total
}

console.log(sum(1, 2, 3)); // => Output: 6
console.log(sum()); // => zero arguments is valid too -- Output: 0
