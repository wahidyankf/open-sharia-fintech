// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
// => this directive is part of the source interface
#ifdef DEBUG
  // => this line makes the program's state or output explicit
  puts("debug=on");
// => this directive is part of the source interface
#else
  // => this line makes the program's state or output explicit
  puts("debug=off");
// => this directive is part of the source interface
#endif
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
