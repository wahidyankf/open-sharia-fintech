// Kata 8 (before): Priority starts at 1, not the default 0 -- Priority[0] has no matching member.
enum Priority {
  Low = 1,
  Medium,
  High,
}

console.log(Priority[0]);
