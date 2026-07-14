// Kata 8 (after): look up Priority.Low itself instead of guessing its underlying numeric value.
enum Priority {
  Low = 1,
  Medium,
  High,
}

console.log(Priority[Priority.Low]);
