// Example 5: Type Error On Mismatch -- assigning a string to a number-typed binding.
let count: number = 42; // => count is 42 (type: number)
count = "oops"; // => TYPE ERROR: a string is not assignable to a number-typed binding
console.log(count); // => never type-checks -- tsc reports the error above first
