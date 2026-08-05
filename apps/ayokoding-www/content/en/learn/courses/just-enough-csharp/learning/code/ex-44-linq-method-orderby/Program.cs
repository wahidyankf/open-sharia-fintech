var xs = new[] { "Lin", "Ada" }; // => source
var ordered = xs.OrderBy(x => x); // => ordering query
Console.WriteLine(string.Join(",", ordered)); // => Output: Ada,Lin
