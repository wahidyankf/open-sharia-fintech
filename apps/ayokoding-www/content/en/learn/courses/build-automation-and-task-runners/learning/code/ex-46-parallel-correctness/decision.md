# Parallel graph correctness

| Graph                                | Consequence                            |
| ------------------------------------ | -------------------------------------- |
| generated.h is a prerequisite of app | compilation waits for the header       |
| app omits generated.h                | a parallel build can compile too early |

A true prerequisite edge, rather than serial command ordering, makes parallel scheduling correct.
