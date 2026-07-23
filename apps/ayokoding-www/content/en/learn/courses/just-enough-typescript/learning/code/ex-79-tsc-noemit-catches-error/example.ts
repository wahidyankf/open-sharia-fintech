// Example 79: tsc --noEmit Catches Error -- the fixed, clean version of this file.
function double(n: number): number {
  // => same signature as broken.ts -- only the multiplication below is fixed
  return n * 2; // => a plain, correctly typed multiplication
}

console.log(double(21)); // => Output: 42
