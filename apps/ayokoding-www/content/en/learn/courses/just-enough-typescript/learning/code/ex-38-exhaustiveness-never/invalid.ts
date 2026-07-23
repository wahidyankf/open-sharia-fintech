// Example 38 (invalid): adding a "triangle" variant without a matching case breaks exhaustiveness.
type Shape =
  | { kind: "circle"; r: number }
  | { kind: "square"; s: number }
  | { kind: "triangle"; base: number; height: number }; // => a NEW, unhandled variant

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      return Math.PI * shape.r ** 2; // => still handled -- circle isn't the problem here
    case "square":
      return shape.s * shape.s; // => still handled -- square isn't the problem either
    default: {
      // => shape here is STILL { kind: "triangle"; ... }, not never -- the switch missed it
      const _exhaustive: never = shape; // => TYPE ERROR: 'triangle' variant is not assignable to never
      return _exhaustive; // => unreachable -- this line never compiles, so it never runs
    }
  }
}

console.log(area({ kind: "triangle", base: 2, height: 3 })); // => never reached -- tsc rejects this file before runtime
