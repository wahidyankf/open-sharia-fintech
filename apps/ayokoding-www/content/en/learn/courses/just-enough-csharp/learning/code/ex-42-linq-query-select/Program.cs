var xs = new[] { "ada", "lin" }; // => source
var upper = from x in xs select x.ToUpper(); // => query projection
Console.WriteLine(string.Join(",", upper)); // => Output: ADA,LIN
