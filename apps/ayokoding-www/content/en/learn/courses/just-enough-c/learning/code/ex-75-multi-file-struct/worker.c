// => this directive is part of the source interface
#include "worker.h"
// => this line makes the program's state or output explicit
int worker_id(const struct Worker *worker) { return worker->id; }
