// Kata 4 (after): extends { length: number } proves T has .length before the body reads it.
function longest<T extends { length: number }>(a: T, b: T): T {
  return a.length >= b.length ? a : b;
}

console.log(longest("hi", "hello"));
