// Example 58: const Object Union -- `as const` + keyof typeof: a modern enum alternative.
const Color = {
  Red: "red", // => a plain object, not an `enum` keyword
  Green: "green",
  Blue: "blue",
} as const; // => as const makes every value a literal, and the whole object readonly

type ColorName = keyof typeof Color; // => ColorName is "Red" | "Green" | "Blue"
type ColorValue = (typeof Color)[ColorName]; // => ColorValue is "red" | "green" | "blue"

const chosen: ColorValue = Color.Green; // => chosen's type is the derived literal union
console.log(chosen); // => Output: green
