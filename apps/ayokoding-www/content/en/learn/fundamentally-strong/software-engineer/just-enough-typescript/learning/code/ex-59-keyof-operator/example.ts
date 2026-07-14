// Example 59: keyof Operator -- keyof T is the union of T's own property names.
type Point = { x: number; y: number };
type PointKey = keyof Point; // => PointKey is exactly "x" | "y"

const key: PointKey = "x"; // => only "x" or "y" satisfy PointKey
console.log(key); // => Output: x
