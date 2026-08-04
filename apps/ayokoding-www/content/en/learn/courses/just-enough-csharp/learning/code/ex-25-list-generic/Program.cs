var names = new List<string> { "Ada" }; // => typed list
names.Add("Lin"); // => grows list
Console.WriteLine(string.Join(",", names)); // => Output: Ada,Lin
