var xs = new List<int> { 1, 2 }; // => mutable source
var query = xs.Where(x => x > 1); // => deferred query
xs.Add(3); // => source changes
Console.WriteLine(string.Join(",", query)); // => Output: 2,3
