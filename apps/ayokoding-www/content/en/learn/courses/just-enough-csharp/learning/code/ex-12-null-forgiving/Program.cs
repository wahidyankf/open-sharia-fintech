string? name = "Ada"; // => locally proven present
Console.WriteLine(name!.Length); // => Output: 3
// => ! suppresses analysis, not a runtime null check
