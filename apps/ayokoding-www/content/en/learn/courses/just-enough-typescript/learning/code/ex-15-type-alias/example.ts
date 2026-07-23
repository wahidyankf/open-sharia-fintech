// Example 15: Type Alias -- `type` names a reusable shape for later use.
type Point = { x: number; y: number }; // => Point is an alias for this exact object shape

const home: Point = { x: 0, y: 0 }; // => a matching literal satisfies Point
console.log(home); // => Output: { x: 0, y: 0 }
