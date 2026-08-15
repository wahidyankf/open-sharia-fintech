// => this directive is part of the source interface
#ifndef WORKER_H
// => this directive is part of the source interface
#define WORKER_H
// => this line makes the program's state or output explicit
struct Worker {
  int id;
};
// => this line makes the program's state or output explicit
int worker_id(const struct Worker *worker);
// => this directive is part of the source interface
#endif
