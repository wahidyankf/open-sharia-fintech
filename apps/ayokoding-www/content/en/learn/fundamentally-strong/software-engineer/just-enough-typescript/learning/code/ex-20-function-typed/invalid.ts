// Example 20 (invalid): a string argument does not satisfy the number parameter type.
function add(a: number, b: number): number {
  return a + b;
}

console.log(add(2, "3")); // => TYPE ERROR: string argument is not assignable to number
