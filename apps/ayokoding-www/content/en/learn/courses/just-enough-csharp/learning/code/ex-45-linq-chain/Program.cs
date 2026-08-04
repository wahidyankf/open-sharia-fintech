var xs = new[] { 3, 1, 2 }; // => source
var result = xs.Where(x => x > 1).Select(x => x * 10).OrderBy(x => x); // => pipeline
Console.WriteLine(string.Join(",", result)); // => Output: 20,30
