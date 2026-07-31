# Content-addressed action key

```text
hash(source bytes, build configuration, declared tools) = action key
```

Changing a declared input changes the key. A build system can use this key to find a result of the
equivalent action without treating a modification time as sufficient identity.
