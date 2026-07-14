// Example 43: Generic Default Param -- <T = string> supplies a type when none is given.
function makeBox<T = string>(value: T): { value: T } {
  // => if the caller never writes <T>, T defaults to string
  return { value };
}

const boxed = makeBox("hi"); // => T is inferred as string anyway, from the argument
console.log(boxed); // => Output: { value: 'hi' }

const empty = makeBox<number>(0); // => explicit T=number overrides the default
console.log(empty); // => Output: { value: 0 }
