// Kata 3 before: The before version runs invalid work; the after version guards execution with availability.
// => Run this file and identify why the behavior violates the UI contract.
var canSave = false;
Console.WriteLine("saved despite " + canSave);
