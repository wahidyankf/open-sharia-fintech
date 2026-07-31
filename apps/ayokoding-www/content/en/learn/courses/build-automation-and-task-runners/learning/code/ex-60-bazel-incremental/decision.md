# Incremental Bazel actions

When a declared source changes, the action keys of actions that consume it change. Independent actions
with unchanged complete inputs retain matching keys and remain eligible for cache reuse.
