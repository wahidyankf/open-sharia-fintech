// Kata 1 before: The before version synchronously waits and models a frozen UI; the after version awaits the task.
// => Run this file and identify why the behavior violates the UI contract.
Thread.Sleep(1);
Console.WriteLine("blocked");
