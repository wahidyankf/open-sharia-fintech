// Example 19 (invalid): "north" is not one of Dir's four allowed literals.
type Dir = "up" | "down" | "left" | "right";
const heading: Dir = "north"; // => TYPE ERROR: "north" is not assignable to Dir
console.log(heading);
