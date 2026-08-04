Console.WriteLine(First(new[] { "a", "b" })); // => Output: a
static T First<T>(IEnumerable<T> xs) => xs.First(); // => type flows through
