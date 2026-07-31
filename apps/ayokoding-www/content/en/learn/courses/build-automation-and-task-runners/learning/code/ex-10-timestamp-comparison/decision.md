# Make timestamp freshness

Make rebuilds a file target when the target is missing or when any declared prerequisite is newer than
that target. It does not compare the bytes of the two files.

`missing(target) OR mtime(prerequisite) > mtime(target) => rebuild`
