// Example 49: Structural Compatibility -- extra fields on a VARIABLE are still assignable.
type Point2D = { x: number; y: number };

const point3D = { x: 1, y: 2, z: 3 }; // => an object with an EXTRA field, held in a variable
const flat: Point2D = point3D; // => OK -- point3D has at least x and y, structurally

console.log(flat); // => Output: { x: 1, y: 2, z: 3 } -- the extra z is still there at runtime
