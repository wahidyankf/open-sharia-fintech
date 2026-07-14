// Example 7: Inference No Annotation -- no type annotation, yet count is still checked.
let count = 5; // => count is 5 (type inferred: number, from the initializer)
count = 10; // => OK -- 10 is also a number
console.log(count); // => Output: 10
