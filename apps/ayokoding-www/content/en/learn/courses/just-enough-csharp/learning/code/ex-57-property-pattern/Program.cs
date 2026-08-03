var point = new Point(0, 4); // => record
Console.WriteLine(point is { X: 0 } ? "axis" : "other"); // => Output: axis

record Point(int X, int Y);
