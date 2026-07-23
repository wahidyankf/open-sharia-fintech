// Kata 1 (after): storing the literal in a variable first sidesteps the excess-property check.
type Point2D = { x: number; y: number };

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

const point3D = { x: 1, y: 2, z: 3 };
printPoint(point3D);
