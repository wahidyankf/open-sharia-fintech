string?[] names = ["Ada", null, "Lin"]; // => nullable source
var sizes = names.Where(x => x is not null).Select(x => x!.Length); // => safe query
Console.WriteLine(string.Join(",", sizes)); // => Output: 3,3
