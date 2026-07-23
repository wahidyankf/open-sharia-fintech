// Example 20: Function Typed -- both parameters and the return value carry annotations.
function add(a: number, b: number): number {
  // => a and b must both be number; the function must return a number
  return a + b; // => a + b's result type (number) matches the declared return type
}

console.log(add(2, 3)); // => Output: 5
