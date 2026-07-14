// Example 29: Narrow With typeof -- typeof splits a union into its constituent branches.
function describe(value: number | string): string {
  if (typeof value === "string") {
    // => inside this branch, value's type is narrowed to just string
    return value.toUpperCase(); // => .toUpperCase() only exists on string
  }
  // => outside the if, value's type is narrowed to just number (the only type left)
  return value.toFixed(2); // => .toFixed() only exists on number
}

console.log(describe("hi")); // => Output: HI
console.log(describe(3.14159)); // => Output: 3.14
