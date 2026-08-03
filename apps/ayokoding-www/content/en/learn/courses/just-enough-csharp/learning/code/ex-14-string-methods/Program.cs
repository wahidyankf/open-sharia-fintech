var text = "ready,steady"; // => source
var parts = text.ToUpper().Split(','); // => transforms and splits
Console.WriteLine($"{parts[1]}:{text.Contains(",")}"); // => Output: STEADY:True
