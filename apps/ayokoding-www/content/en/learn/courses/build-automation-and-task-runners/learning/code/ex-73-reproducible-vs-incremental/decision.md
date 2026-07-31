# Two distinct build qualities

| Quality      | Question                                           |
| ------------ | -------------------------------------------------- |
| Incremental  | which already-complete work may be skipped?        |
| Reproducible | do equivalent declared inputs produce equal bytes? |

An incremental build can still be non-reproducible if an undeclared host input changes its result.
