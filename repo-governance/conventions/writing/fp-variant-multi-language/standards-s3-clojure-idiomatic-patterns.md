---
description: The Clojure language patterns (namespaced-keyword maps, spec/malli, sequences and transducers, multimethods, threading macros, atoms/refs/agents, protocols) required in the Clojure tab.
when_to_use: Use when writing or reviewing the Clojure tab of an FP-variant example, to confirm it uses native Clojure idioms rather than F#-influenced equivalents.
---

# Standards S3: Clojure Idiomatic Patterns

Clojure code in these tutorials MUST remain idiomatic to the Clojure community and runtime. The following patterns are expected to appear at the appropriate complexity level and MUST NOT be replaced by F#-influenced equivalents:

- **Maps with namespaced keywords** — domain entities as plain maps using `::entity/field` namespaced keywords; `assoc`, `dissoc`, `update`, `merge` for structural transformation.
- **Specs or malli schemas for validation** — `clojure.spec.alpha` `s/def` + `s/valid?` + `s/explain`, or `malli` schema definitions, to enforce domain invariants.
- **Sequences and transducers** — `map`, `filter`, `reduce`, `into`, `transduce` over lazy sequences; transducer composition with `comp` for efficient pipeline processing.
- **Multimethods** — `defmulti` + `defmethod` for open dispatch on arbitrary criteria; the idiomatic Clojure approach to polymorphism that does not require a type hierarchy.
- **Threading macros** — `->` (thread-first) and `->>` (thread-last) for left-to-right data transformation pipelines; `as->` for non-uniform threading.
- **Atoms, refs, and agents** — `atom` for uncoordinated synchronous state; `ref` + `dosync` for coordinated transactional state; `agent` for asynchronous independent state.
- **Protocols** — `defprotocol` + `extend-protocol` or `reify` for polymorphic dispatch over existing types; the idiomatic Clojure alternative to interfaces.
- **REPL-friendly data orientation** — functions that accept and return plain data (maps, vectors, sets, lists); no hidden class coupling; results that print legibly in a REPL session.
- **Namespace organisation** — `ns` declarations with `:require` aliases; `defn` at the top level; namespace-qualified symbols for public APIs.
- **`core.async` channels** — `go` blocks, `chan`, `<!`, `>!` for asynchronous workflows when concurrency is part of the example concept.

Clojure code that simulates discriminated unions as tagged maps (`{:tag :ok :value x}`) is acceptable only when the example specifically teaches that pattern; it MUST include an annotation noting this is the Clojure data-orientation approach (see S5).
