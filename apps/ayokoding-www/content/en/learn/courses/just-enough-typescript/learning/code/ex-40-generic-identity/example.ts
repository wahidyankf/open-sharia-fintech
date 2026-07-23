// Example 40: Generic Identity -- <T> lets one function work across every type, safely.
function identity<T>(value: T): T {
  // => T is inferred from whatever argument is actually passed at each call-site
  return value; // => the return type is exactly T -- no widening to `any` or `unknown`
}

const num = identity(42); // => T is inferred as number -- num's type is number
const str = identity("hi"); // => T is inferred as string -- str's type is string
console.log(num, str); // => Output: 42 hi
