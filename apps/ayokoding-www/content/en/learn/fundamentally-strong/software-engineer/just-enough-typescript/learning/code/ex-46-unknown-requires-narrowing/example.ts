// Example 46: unknown Requires Narrowing -- unknown is the safe top type: nothing works until checked.
let payload: unknown = "hello"; // => payload could be ANY value at all -- its type is unknown

if (typeof payload === "string") {
  // => only after this check is payload narrowed to string
  console.log(payload.toUpperCase()); // => .toUpperCase() is now safe -- Output: HELLO
}
