var point = new Point(2, 3); // => immutable data
Console.WriteLine(point.X + point.Y); // => Output: 5

record Point(int X, int Y);
