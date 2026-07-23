// Example 19: Literal Union -- Dir is restricted to exactly these four string literals.
type Dir = "up" | "down" | "left" | "right"; // => only these four exact strings are valid

const heading: Dir = "up"; // => "up" is one of the four allowed literals
console.log(heading); // => Output: up
