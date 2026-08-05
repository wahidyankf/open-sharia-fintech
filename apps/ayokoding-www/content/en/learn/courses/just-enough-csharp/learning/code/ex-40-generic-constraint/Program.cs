Console.WriteLine(Max(2, 5)); // => Output: 5
static T Max<T>(T a, T b)
    where T : IComparable<T> => a.CompareTo(b) > 0 ? a : b; // => constraint
