---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish C's compile/run loop, core scalar types, operators, control flow, functions, formatted I/O, scope, arrays, strings, and basic preprocessing. Each entry is self-contained, heavily annotated, and copy-paste runnable.

## Example 1: GCC Compiles a Source File

_ex-01 · exercises co-01_

Compile one source file into a binary. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-01-gcc-compile/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    puts("Hello from C!");
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
Hello from C!
```

**Key takeaway**: Compile one source file into a binary. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Compile one source file into a binary. Use the compiler's warning flags from the first command.

---

## Example 2: Run the Compiled Binary

_ex-02 · exercises co-01_

Run the executable that the compiler produced. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-02-run-binary/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    puts("The binary ran.");
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
The binary ran.
```

**Key takeaway**: Run the executable that the compiler produced. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Run the executable that the compiler produced. Use the compiler's warning flags from the first command.

---

## Example 3: Clang Compiles the Same Program

_ex-03 · exercises co-01_

Compile the same standard C source with Clang. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-03-clang-compile/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    puts("Clang-compatible source.");
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
Clang-compatible source.
```

**Key takeaway**: Compile the same standard C source with Clang. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Compile the same standard C source with Clang. Use the compiler's warning flags from the first command.

---

## Example 4: main Returns a Process Status

_ex-04 · exercises co-04_

Return zero from main to report success. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-04-main-return/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    puts("success");
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
success
```

**Key takeaway**: Return zero from main to report success. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Return zero from main to report success. Use the compiler's warning flags from the first command.

---

## Example 5: An int Variable

_ex-05 · exercises co-05_

Declare an integer and print its value. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-05-int-var/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int count = 42;
// => this executable statement makes the example observable
    printf("%d\n", count);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
42
```

**Key takeaway**: Declare an integer and print its value. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Declare an integer and print its value. Use the compiler's warning flags from the first command.

---

## Example 6: A char Variable

_ex-06 · exercises co-05_

Store one character in a char. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-06-char-var/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    char language = 'C';
// => this executable statement makes the example observable
    printf("%c\n", language);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
C
```

**Key takeaway**: Store one character in a char. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Store one character in a char. Use the compiler's warning flags from the first command.

---

## Example 7: float and double

_ex-07 · exercises co-05_

Compare float and double formatting. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-07-float-double/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    float small = 3.5f;
// => this executable statement makes the example observable
    double precise = 3.5;
// => this executable statement makes the example observable
    printf("float=%.1f double=%.1f\n", small, precise);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
float=3.5 double=3.5
```

**Key takeaway**: Compare float and double formatting. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Compare float and double formatting. Use the compiler's warning flags from the first command.

---

## Example 8: Arithmetic Operators

_ex-08 · exercises co-07_

Add values and retain a remainder. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-08-arithmetic/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int left = 7;
// => this executable statement makes the example observable
    int right = 3;
// => this executable statement makes the example observable
    printf("sum=%d remainder=%d\n", left + right, left % right);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
sum=10 remainder=1
```

**Key takeaway**: Add values and retain a remainder. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Add values and retain a remainder. Use the compiler's warning flags from the first command.

---

## Example 9: Comparison and Logical Operators

_ex-09 · exercises co-07_

Combine comparisons into a truth value. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-09-comparison-logical/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int age = 20;
// => this executable statement makes the example observable
    int allowed = age >= 18 && age < 65;
// => this executable statement makes the example observable
    printf("allowed=%d\n", allowed);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
allowed=1
```

**Key takeaway**: Combine comparisons into a truth value. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Combine comparisons into a truth value. Use the compiler's warning flags from the first command.

---

## Example 10: Bitwise Operators

_ex-10 · exercises co-07_

Build a bit mask with shifts and OR. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-10-bitwise/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    unsigned int mask = (1u << 0) | (1u << 2);
// => this executable statement makes the example observable
    printf("mask=%u\n", mask);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
mask=5
```

**Key takeaway**: Build a bit mask with shifts and OR. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Build a bit mask with shifts and OR. Use the compiler's warning flags from the first command.

---

## Example 11: if and else

_ex-11 · exercises co-08_

Choose one branch from a condition. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-11-if-else/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int temperature = 24;
// => this executable statement makes the example observable
    if (temperature > 20) {
// => this executable statement makes the example observable
        puts("warm");
// => this executable statement makes the example observable
    } else {
// => this executable statement makes the example observable
        puts("cool");
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
warm
```

**Key takeaway**: Choose one branch from a condition. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Choose one branch from a condition. Use the compiler's warning flags from the first command.

---

## Example 12: switch Dispatch

_ex-12 · exercises co-08_

Dispatch a small integer to a case. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-12-switch/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int command = 2;
// => this executable statement makes the example observable
    switch (command) {
// => this executable statement makes the example observable
    case 1: puts("read"); break;
// => this executable statement makes the example observable
    case 2: puts("write"); break;
// => this executable statement makes the example observable
    default: puts("unknown"); break;
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
write
```

**Key takeaway**: Dispatch a small integer to a case. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Dispatch a small integer to a case. Use the compiler's warning flags from the first command.

---

## Example 13: A for Loop

_ex-13 · exercises co-08_

Repeat a counted operation. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-13-for-loop/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    for (int index = 0; index < 3; ++index) {
// => this executable statement makes the example observable
        printf("%d%s", index, index == 2 ? "\n" : " ");
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
0 1 2
```

**Key takeaway**: Repeat a counted operation. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Repeat a counted operation. Use the compiler's warning flags from the first command.

---

## Example 14: A while Loop

_ex-14 · exercises co-08_

Repeat while a condition remains true. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-14-while-loop/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int remaining = 3;
// => this executable statement makes the example observable
    while (remaining > 0) {
// => this executable statement makes the example observable
        printf("%d%s", remaining, remaining == 1 ? "\n" : " ");
// => this executable statement makes the example observable
        --remaining;
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
3 2 1
```

**Key takeaway**: Repeat while a condition remains true. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Repeat while a condition remains true. Use the compiler's warning flags from the first command.

---

## Example 15: Define and Call a Function

_ex-15 · exercises co-09_

Call a function that returns a calculation. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-15-function-def/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
static int square(int value) {
// => this executable statement makes the example observable
    return value * value;
// => this executable statement makes the example observable
}
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    printf("%d\n", square(3));
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
9
```

**Key takeaway**: Call a function that returns a calculation. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Call a function that returns a calculation. Use the compiler's warning flags from the first command.

---

## Example 16: A Forward Function Prototype

_ex-16 · exercises co-09_

Declare a function before main uses it. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-16-function-prototype/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
static int add(int left, int right);
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    printf("%d\n", add(3, 4));
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
// => this executable statement makes the example observable
static int add(int left, int right) {
// => this executable statement makes the example observable
    return left + right;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
7
```

**Key takeaway**: Declare a function before main uses it. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Declare a function before main uses it. Use the compiler's warning flags from the first command.

---

## Example 17: printf Format Specifiers

_ex-17 · exercises co-17_

Format an integer, string, and floating value. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-17-printf-format/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int id = 7;
// => this executable statement makes the example observable
    const char *name = "ada";
// => this executable statement makes the example observable
    double score = 9.5;
// => this executable statement makes the example observable
    printf("id=%d name=%s score=%.1f\n", id, name, score);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
id=7 name=ada score=9.5
```

**Key takeaway**: Format an integer, string, and floating value. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Format an integer, string, and floating value. Use the compiler's warning flags from the first command.

---

## Example 18: scanf Reads an Integer

_ex-18 · exercises co-18_

Read one integer from standard input. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-18-scanf-input/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int value = 0;
// => this executable statement makes the example observable
    if (scanf("%d", &value) == 1) {
// => this executable statement makes the example observable
        printf("doubled=%d\n", value * 2);
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`; use `printf "4\\n" | ./example` for the shown input.

**Expected output**:

```text
doubled=8
```

**Key takeaway**: Read one integer from standard input. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Read one integer from standard input. Use the compiler's warning flags from the first command.

---

## Example 19: Block Scope

_ex-19 · exercises co-06_

Keep a temporary variable inside braces. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-19-scope-block/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int outer = 1;
// => this executable statement makes the example observable
    {
// => this executable statement makes the example observable
        int inner = 2;
// => this executable statement makes the example observable
        printf("inside=%d outside=%d\n", inner, outer);
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
inside=2 outside=1
```

**Key takeaway**: Keep a temporary variable inside braces. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Keep a temporary variable inside braces. Use the compiler's warning flags from the first command.

---

## Example 20: sizeof Reports Bytes

_ex-20 · exercises co-25_

Ask for the storage size of types. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-20-sizeof/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
struct Pair { int left; int right; };
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    printf("int=%zu pair=%zu\n", sizeof(int), sizeof(struct Pair));
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
int and Pair byte counts
```

**Key takeaway**: Ask for the storage size of types. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Ask for the storage size of types. Use the compiler's warning flags from the first command.

---

## Example 21: const Prevents Reassignment

_ex-21 · exercises co-25_

Declare a value this program will not modify. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-21-const/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    const int limit = 10;
// => this executable statement makes the example observable
    printf("limit=%d\n", limit);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
limit=10
```

**Key takeaway**: Declare a value this program will not modify. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Declare a value this program will not modify. Use the compiler's warning flags from the first command.

---

## Example 22: Declare and Index an Array

_ex-22 · exercises co-12_

Store fixed-length integer elements. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-22-array-declare/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int values[3] = {10, 20, 30};
// => this executable statement makes the example observable
    printf("middle=%d\n", values[1]);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
middle=20
```

**Key takeaway**: Store fixed-length integer elements. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Store fixed-length integer elements. Use the compiler's warning flags from the first command.

---

## Example 23: Loop Through an Array

_ex-23 · exercises co-12, co-08_

Traverse every array element by index. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-23-array-loop/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    int values[] = {1, 2, 3};
// => this executable statement makes the example observable
    int sum = 0;
// => this executable statement makes the example observable
    for (size_t index = 0; index < 3; ++index) {
// => this executable statement makes the example observable
        sum += values[index];
// => this executable statement makes the example observable
    }
// => this executable statement makes the example observable
    printf("sum=%d\n", sum);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
sum=6
```

**Key takeaway**: Traverse every array element by index. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Traverse every array element by index. Use the compiler's warning flags from the first command.

---

## Example 24: A Null-Terminated C String

_ex-24 · exercises co-14_

Store text in a writable char array. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-24-string-literal/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    char greeting[] = "hello";
// => this executable statement makes the example observable
    printf("%s\n", greeting);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
hello
```

**Key takeaway**: Store text in a writable char array. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Store text in a writable char array. Use the compiler's warning flags from the first command.

---

## Example 25: Include stdio Declarations

_ex-25 · exercises co-20_

Include the header that declares printf. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-25-include-stdio/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    puts("stdio is included");
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
stdio is included
```

**Key takeaway**: Include the header that declares printf. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Include the header that declares printf. Use the compiler's warning flags from the first command.

---

## Example 26: A #define Constant

_ex-26 · exercises co-21_

Replace a symbolic constant during preprocessing. This keeps one machine-visible rule small enough to inspect before it appears inside a systems program.

**`learning/code/ex-26-define-const/example.c`**

```c
// => preprocessor directive needed by this translation unit
#include <stdio.h>
// => preprocessor directive needed by this translation unit
#define PORT 8080
// => this executable statement makes the example observable
int main(void) {
// => this executable statement makes the example observable
    printf("port=%d\n", PORT);
// => this executable statement makes the example observable
    return 0;
// => this executable statement makes the example observable
}
```

**Run**: `cc -std=c17 -Wall -Wextra -pedantic example.c -o example && ./example`.

**Expected output**:

```text
port=8080
```

**Key takeaway**: Replace a symbolic constant during preprocessing. Use the compiler's warning flags from the first command.

**Why it matters**: Later OS and systems examples combine this rule with pointers, files, and build tools. Seeing it in a complete, dependency-free program makes the observed result explainable instead of magical, and gives you a command that can reproduce the behavior when you change it. That repeatable loop lets you compare compiler behavior, inspect changes, and diagnose a systems failure before it reaches production. The specific practice in this example is: Replace a symbolic constant during preprocessing. Use the compiler's warning flags from the first command.

---
