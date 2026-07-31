# Build-tool selection

| Need                                         | Suitable starting point |
| -------------------------------------------- | ----------------------- |
| named local developer command                | just or npm script      |
| transparent timestamp file graph             | GNU Make                |
| hermetic large target graph and shared cache | Bazel or Gradle         |

Start with the model the project needs; do not add a stronger tool merely because it exists.
