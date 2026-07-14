// Example 34: User-Defined Type Guard -- a predicate function narrows at the call-site.
type Cat = { kind: "cat"; meow(): string };
type Dog = { kind: "dog"; bark(): string };
type Animal = Cat | Dog;

function isCat(a: Animal): a is Cat {
  // => `a is Cat` tells the compiler: when this returns true, a is narrowed to Cat
  return a.kind === "cat"; // => the actual runtime check backing the type predicate
}

function speak(a: Animal): string {
  if (isCat(a)) {
    // => after calling isCat(a), a is narrowed to Cat inside this branch
    return a.meow(); // => .meow() only exists on Cat
  }
  return a.bark(); // => here, a is narrowed to Dog
}

const felix: Cat = { kind: "cat", meow: () => "meow!" };
console.log(speak(felix)); // => Output: meow!
