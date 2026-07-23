// Example 79 (broken): the SAME function, with a deliberate type error introduced.
function double(n: number): number {
  return n * "2"; // => TYPE ERROR: arithmetic on a number and a string
}

console.log(double(21)); // => never reached -- tsc rejects this file before it can run
