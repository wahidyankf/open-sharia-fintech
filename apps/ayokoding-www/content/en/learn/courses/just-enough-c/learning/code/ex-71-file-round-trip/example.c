// => this directive is part of the source interface
#include <stdio.h>
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  FILE *file = tmpfile();
  // => this line makes the program's state or output explicit
  char message[8] = {0};
  // => this line makes the program's state or output explicit
  if (file == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  fputs("ok\n", file);
  // => this line makes the program's state or output explicit
  rewind(file);
  // => this line makes the program's state or output explicit
  if (fgets(message, sizeof message, file) == NULL)
    return 1;
  // => this line makes the program's state or output explicit
  fclose(file);
  // => this line makes the program's state or output explicit
  printf("message=%s", message);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
