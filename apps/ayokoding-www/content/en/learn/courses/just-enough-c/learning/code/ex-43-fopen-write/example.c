// => this directive makes a declaration available
#include <stdio.h>
// => this line is part of the complete runnable program
int main(void) {
  // => this line is part of the complete runnable program
  FILE *file = tmpfile();
  // => this line is part of the complete runnable program
  if (file == NULL)
    return 1;
  // => this line is part of the complete runnable program
  fprintf(file, "written\n");
  // => this line is part of the complete runnable program
  fclose(file);
  // => this line is part of the complete runnable program
  puts("written");
  // => this line is part of the complete runnable program
  return 0;
  // => this line is part of the complete runnable program
}
