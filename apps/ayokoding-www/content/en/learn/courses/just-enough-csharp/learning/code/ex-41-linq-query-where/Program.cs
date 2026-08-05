var xs = new[] { -1, 2, 3 }; // => source
var positive = from x in xs where x > 0 select x; // => query filter
Console.WriteLine(string.Join(",", positive)); // => Output: 2,3
