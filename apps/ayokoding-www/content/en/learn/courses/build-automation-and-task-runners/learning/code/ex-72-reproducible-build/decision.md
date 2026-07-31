# Reproducible build requirements

| Requirement                   | Purpose               |
| ----------------------------- | --------------------- |
| pinned tools and dependencies | same intended inputs  |
| hermetic action boundary      | no hidden host inputs |
| deterministic output process  | same result bytes     |

A cache can reuse work, but reproducibility concerns equality of output from equivalent inputs.
