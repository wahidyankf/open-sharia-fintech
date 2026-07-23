// Example 41: Generic Array First -- a generic helper that works on an array of any T.
function first<T>(xs: T[]): T | undefined {
  // => returns the first element, or undefined when xs is empty -- T flows through
  return xs[0];
}

const n = first([10, 20, 30]); // => T is inferred as number -- n's type is number | undefined
console.log(n); // => Output: 10
console.log(first<string>([])); // => explicit T=string, empty array -- Output: undefined
