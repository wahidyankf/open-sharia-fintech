// Example 35: Assertion Function -- `asserts x is T` narrows AFTER the call, not inside a branch.
function assertString(x: unknown): asserts x is string {
  // => if x is not a string, this throws; if it returns normally, x IS a string
  if (typeof x !== "string") {
    throw new Error("expected a string"); // => aborts execution -- narrowing never "escapes" a throw
  }
}

function shout(value: unknown): string {
  assertString(value); // => after this line, value's type is narrowed to string
  return value.toUpperCase(); // => .toUpperCase() is safe -- the assertion already ran
}

console.log(shout("hi")); // => Output: HI
