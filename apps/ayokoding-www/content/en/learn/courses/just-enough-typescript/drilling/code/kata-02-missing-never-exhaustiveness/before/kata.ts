// Kata 2 (before): a NEW "triangle" variant was added, but the switch was never updated --
// the never-typed exhaustiveness check catches the gap at compile time.
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "triangle"; base: number; height: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2;
    case "square":
      return shape.s * shape.s;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}

console.log(area({ kind: "triangle", base: 4, height: 3 }));
