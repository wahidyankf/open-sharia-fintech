// Kata 2 (after): a "triangle" case handles the new variant -- the switch is exhaustive again.
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
    case "triangle":
      return (shape.base * shape.height) / 2;
    default: {
      const _exhaustive: never = shape;
      return _exhaustive;
    }
  }
}

console.log(area({ kind: "triangle", base: 4, height: 3 }));
