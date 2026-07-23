// Kata 4 (before): T has no constraint, so the compiler can't prove it has a .length at all.
function longest<T>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(longest("hi", "hello"));
