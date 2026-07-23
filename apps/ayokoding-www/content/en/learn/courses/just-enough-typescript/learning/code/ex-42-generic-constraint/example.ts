// Example 42: Generic Constraint -- `extends` restricts T to shapes that have a length.
function longest<T extends { length: number }>(a: T, b: T): T {
  // => T must have a .length property -- strings and arrays both qualify
  return a.length >= b.length ? a : b; // => .length is safe to read on any T here
}

console.log(longest("hi", "hello")); // => Output: hello
console.log(longest([1, 2], [1, 2, 3])); // => Output: [ 1, 2, 3 ]
