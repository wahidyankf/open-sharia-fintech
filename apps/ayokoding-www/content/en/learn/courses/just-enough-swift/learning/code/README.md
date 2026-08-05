# Swift example runners

The learning pages are the annotated primary source. Each `ex-NN` fenced Swift block is a
copy-paste-ready program except the explicitly marked REPL and intentional compiler/trap demos.
For a normal example, save the block as `Example.swift` and run either command:

```sh
swift Example.swift
swiftc Example.swift -o example && ./example
```

The compiler-rejection and force-unwrap examples keep their failing line commented so every pasted
file remains runnable. Uncomment only to observe the documented diagnostic or runtime trap. The
materialized capstone source lives in `../capstone/code/` and compiles with `swiftc Main.swift -o availability`.
