try
{
    throw new BalanceException("insufficient");
} // => domain failure
catch (BalanceException e)
{
    Console.WriteLine(e.Message);
} // => Output: insufficient

class BalanceException(string message) : Exception(message);
