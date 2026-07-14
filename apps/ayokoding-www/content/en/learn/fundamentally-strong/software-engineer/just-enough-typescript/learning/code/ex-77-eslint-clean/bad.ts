// Example 77: eslint Clean -- bad.ts has a genuine unused variable.
function greet(name: string): string {
  const unused = "never read"; // => eslint's no-unused-vars rule flags exactly this
  return `hi ${name}`; // => the function itself still works correctly
}

console.log(greet("Ada")); // => Output: hi Ada -- the SCRIPT runs fine; eslint still flags it
