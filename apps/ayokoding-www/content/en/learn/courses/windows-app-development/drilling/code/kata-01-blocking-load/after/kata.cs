// Kata 1 after: The before version synchronously waits and models a frozen UI; the after version awaits the task.
// => Run this file and compare the bounded, observable result.
await Task.Delay(1);
Console.WriteLine("responsive");
