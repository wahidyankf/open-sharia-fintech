// Example 37: Discriminated Switch -- switch(shape.kind) narrows inside every case.
type Shape = { kind: "circle"; r: number } | { kind: "square"; s: number };

function area(shape: Shape): number {
  switch (shape.kind) {
    case "circle":
      // => here, shape is narrowed to the circle variant -- .r is safe
      return Math.PI * shape.r ** 2;
    case "square":
      // => here, shape is narrowed to the square variant -- .s is safe
      return shape.s * shape.s;
  }
}

console.log(area({ kind: "square", s: 4 })); // => Output: 16
console.log(area({ kind: "circle", r: 1 }).toFixed(2)); // => Output: 3.14
