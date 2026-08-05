var result = new Result(true, "saved"); // => record
Console.WriteLine(
    result switch
    {
        { Ok: true } => "ok",
        _ => "retry",
    }
); // => Output: ok

record Result(bool Ok, string Message);
