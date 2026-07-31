# CI cache sequence

1. Compute a key from complete declared build inputs.
2. Restore a matching cache, if available.
3. Invoke the build tool.
4. Save reusable output after a successful build.

The cache boundary must match the build tool's correctness boundary.
