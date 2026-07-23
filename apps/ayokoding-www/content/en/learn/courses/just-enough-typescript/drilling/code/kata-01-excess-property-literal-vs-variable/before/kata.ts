// Kata 1 (before): an object literal with an extra field fails excess-property checking.
type Point2D = { x: number; y: number };

function printPoint(p: Point2D): void {
  console.log(`(${p.x}, ${p.y})`);
}

printPoint({ x: 1, y: 2, z: 3 });
