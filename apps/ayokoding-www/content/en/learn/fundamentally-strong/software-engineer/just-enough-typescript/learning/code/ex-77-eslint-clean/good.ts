// Example 77 (fixed): the unused variable is removed entirely.
function greet(name: string): string {
  return `hi ${name}`; // => no dead binding left behind
}

console.log(greet("Ada")); // => Output: hi Ada
