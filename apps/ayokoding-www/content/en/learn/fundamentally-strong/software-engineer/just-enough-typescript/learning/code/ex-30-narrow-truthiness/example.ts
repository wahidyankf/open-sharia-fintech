// Example 30: Narrow Truthiness -- a plain `if (x)` check narrows away undefined.
function shout(text: string | undefined): string {
  if (text) {
    // => inside this branch, text's type is narrowed from `string | undefined` to `string`
    return text.toUpperCase() + "!"; // => .toUpperCase() is safe -- text cannot be undefined here
  }
  return "(nothing to shout)"; // => this branch runs when text was undefined or ""
}

console.log(shout("hello")); // => Output: HELLO!
console.log(shout(undefined)); // => Output: (nothing to shout)
