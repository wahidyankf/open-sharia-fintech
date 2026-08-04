var xs = new[] { 1, 2, 3, 4 }; // => source
var even = xs.Where(x => x % 2 == 0); // => method filter
Console.WriteLine(string.Join(",", even)); // => Output: 2,4
