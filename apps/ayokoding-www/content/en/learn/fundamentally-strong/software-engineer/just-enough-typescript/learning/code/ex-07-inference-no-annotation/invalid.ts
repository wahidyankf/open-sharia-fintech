// Example 7 (invalid): reassigning the inferred number binding with a string.
let count = 5; // => count's type is inferred as number
count = "six"; // => TYPE ERROR: a string is not assignable to the inferred number type
console.log(count);
