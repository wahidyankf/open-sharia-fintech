// Example 78: prettier Format -- messy.ts, deliberately misformatted input.
function add(a: number, b: number): number {
  return a + b; // => same logic as before -- prettier only changed style
}

console.log(add(1, 2)); // => same call as before -- only whitespace/semicolons changed
