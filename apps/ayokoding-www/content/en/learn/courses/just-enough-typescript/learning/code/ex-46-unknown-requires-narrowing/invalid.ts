// Example 46 (invalid): calling a method on unknown before narrowing it.
let payload: unknown = "hello";

console.log(payload.toUpperCase()); // => TYPE ERROR: 'payload' is of type 'unknown'
