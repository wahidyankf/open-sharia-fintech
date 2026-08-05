var score = 82; // => input
var result = score switch
{
    >= 80 => "distinction",
    >= 50 => "pass",
    _ => "retry",
};
Console.WriteLine(result); // => Output: pass
