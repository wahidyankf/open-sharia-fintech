// Example 27: Typed Callback Param -- Array.prototype.map infers the element type for you.
const nums: number[] = [1, 2, 3]; // => nums is number[]

const doubled = nums.map((n) => n * 2); // => n is inferred as number -- no annotation written
console.log(doubled); // => Output: [ 2, 4, 6 ]
