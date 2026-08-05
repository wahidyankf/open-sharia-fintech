var xs = new List<int> { 1, 2 }; // => source
var snapshot = xs.Where(x => x > 1).ToList(); // => immediate list
xs.Add(3); // => later change
Console.WriteLine(string.Join(",", snapshot)); // => Output: 2
