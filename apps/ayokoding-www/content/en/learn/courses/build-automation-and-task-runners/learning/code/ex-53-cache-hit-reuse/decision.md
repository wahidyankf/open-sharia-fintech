# Cache hit reuse

| Cache lookup                         | Action outcome                 |
| ------------------------------------ | ------------------------------ |
| complete key matches a stored result | restore the stored output      |
| key does not match                   | execute and store a new output |

The key must include every relevant declared input or reuse can return stale output.
