var names = new[] { "Ada", "Lin" }; // => source
var initials = names.Select(name => name[0]); // => lambda projection
Console.WriteLine(string.Join(",", initials)); // => Output: A,L
