var point = new Point(3, 4); // => record
var (x, y) = point; // => deconstruction
Console.WriteLine(x + y); // => Output: 7

record Point(int X, int Y);
