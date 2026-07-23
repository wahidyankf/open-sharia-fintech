// Example 18: Union Type -- Id is EITHER a number OR a string.
type Id = number | string; // => a value assignable to Id is any number, or any string

const numericId: Id = 42; // => a number satisfies the union
const textId: Id = "user-42"; // => a string ALSO satisfies the union
console.log(numericId, textId); // => Output: 42 user-42
