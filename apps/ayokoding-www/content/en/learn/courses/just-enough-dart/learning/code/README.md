# Dart example runners

The learning pages are the annotated primary source. Each `ex-NN` Dart block is a complete,
copy-paste-ready program except explicitly marked command, compiler-rejection, and runtime-trap
demos. Save a normal block as `example.dart` and run:

```bash
dart run example.dart
```

For a compiler-rejection demo, uncomment the marked failing line and run `dart analyze example.dart`.
For the `!` trap demo, uncomment only after reading its warning. The materialized capstone source
lives in `../capstone/code/`; from that directory run `dart pub get`, `dart run`, and `dart test`.
