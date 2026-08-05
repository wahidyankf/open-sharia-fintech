var move = (0, 1); // => tuple
var label = move switch
{
    (0, 0) => "still",
    (0, _) => "vertical",
    _ => "other",
}; // => match
Console.WriteLine(label); // => Output: vertical
