var values = new List<int> { 1, 2 };
var snapshot = values.Where(value => value > 1).ToList();
values.Add(3);
Console.WriteLine(string.Join(",", snapshot)); // => Output: 2
