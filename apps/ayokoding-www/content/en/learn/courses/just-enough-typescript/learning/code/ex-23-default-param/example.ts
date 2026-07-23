// Example 23: Default Param -- exp = 2 supplies a value whenever the caller omits it.
function pow(base: number, exp: number = 2): number {
  // => exp's type is inferred as number from its default value 2
  return base ** exp; // => exponentiation
}

console.log(pow(3)); // => exp omitted, defaults to 2 -- Output: 9
console.log(pow(2, 5)); // => exp explicitly 5 -- Output: 32
