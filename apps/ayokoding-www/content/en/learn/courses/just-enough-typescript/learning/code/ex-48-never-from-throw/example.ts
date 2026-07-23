// Example 48: never From Throw -- a function that always throws never actually returns.
function fail(message: string): never {
  // => never means "this function's return type is impossible to observe" -- it always throws
  throw new Error(message); // => execution never reaches a return statement
}

function getOrFail(value: string | undefined): string {
  if (value === undefined) {
    fail("value was required"); // => TS knows fail() never returns, so no return is needed here
  }
  return value; // => value is narrowed to string -- fail()'s never lets this branch narrow too
}

console.log(getOrFail("present")); // => Output: present
