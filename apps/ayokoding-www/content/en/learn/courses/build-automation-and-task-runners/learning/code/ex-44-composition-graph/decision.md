# Composed verification

The verify task reports success only after both leaf tasks complete successfully.

```text
verify
├── lint
└── test
```

The diagram names command dependencies. It does not imply timestamp-based reuse.
