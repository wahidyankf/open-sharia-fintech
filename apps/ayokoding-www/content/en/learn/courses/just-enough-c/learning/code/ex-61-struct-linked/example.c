// => this directive is part of the source interface
#include <stdio.h>
// => this directive is part of the source interface
#include <stdlib.h>
// => this line makes the program's state or output explicit
struct Node {
  int value;
  struct Node *next;
};
// => this line makes the program's state or output explicit
int main(void) {
  // => this line makes the program's state or output explicit
  struct Node *first = malloc(sizeof *first);
  // => this line makes the program's state or output explicit
  struct Node *second = malloc(sizeof *second);
  // => this line makes the program's state or output explicit
  if (first == NULL || second == NULL) {
    free(first);
    free(second);
    return 1;
  }
  // => this line makes the program's state or output explicit
  first->value = 1;
  first->next = second;
  // => this line makes the program's state or output explicit
  second->value = 2;
  second->next = NULL;
  // => this line makes the program's state or output explicit
  for (struct Node *node = first; node != NULL; node = node->next) {
    // => this line makes the program's state or output explicit
    printf("%d%s", node->value, node->next == NULL ? "\n" : " ");
    // => this line makes the program's state or output explicit
  }
  // => this line makes the program's state or output explicit
  free(second);
  free(first);
  // => this line makes the program's state or output explicit
  return 0;
  // => this line makes the program's state or output explicit
}
