// Example 38: Exhaustiveness Never -- a `never`-typed default catches any unhandled variant.
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number }; // => two variants, tagged by "kind"

function area(shape: Shape): number {
  switch (shape.kind) {
    // => TypeScript checks exhaustiveness against every case below
    case "circle":
      return Math.PI * shape.r ** 2; // => narrowed to the circle variant here -- .r is safe
    case "square":
      return shape.s * shape.s; // => narrowed to the square variant here -- .s is safe
    default: {
      // => if every case above is handled, shape's type here narrows to never
      const _exhaustive: never = shape; // => only compiles if NO variant reaches here
      return _exhaustive; // => unreachable at runtime -- exists purely for the compiler
    }
  }
}

console.log(area({ kind: "circle", r: 2 }).toFixed(2)); // => Output: 12.57
