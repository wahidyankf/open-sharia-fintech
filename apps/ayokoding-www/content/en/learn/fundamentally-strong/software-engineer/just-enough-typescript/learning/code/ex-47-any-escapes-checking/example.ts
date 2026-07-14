// Example 47: any Escapes Checking -- any opts a value out of type checking entirely.
let payload: any = "hello"; // => payload's type is any -- the compiler stops checking it

console.log(payload.toUpperCase()); // => compiles even though .toUpperCase() is unverified
console.log(payload.thisMethodDoesNotExist()); // => ALSO compiles -- any allows anything
// => Output (runtime): HELLO, then a real TypeError (any hides the bug until runtime)
