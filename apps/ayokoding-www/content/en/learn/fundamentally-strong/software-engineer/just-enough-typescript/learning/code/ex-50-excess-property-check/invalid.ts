// Example 50 (invalid): a literal passed directly with an extra field triggers excess-property checking.
type Point2D = { x: number; y: number };

const flat: Point2D = { x: 1, y: 2, z: 3 }; // => TYPE ERROR: 'z' does not exist on Point2D
console.log(flat);
