var first = new Point(1, 2); // => original
var moved = first with { X = 5 }; // => changed copy
Console.WriteLine(first.X + ":" + moved.X); // => Output: 1:5

record Point(int X, int Y);
