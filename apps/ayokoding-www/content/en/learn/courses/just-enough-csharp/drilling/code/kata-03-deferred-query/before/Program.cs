var values = new List<int> { 1, 2 };
var query = values.Where(value => value > 1);
values.Add(3);
Console.WriteLine(string.Join(",", query)); // => unstable: 2,3
