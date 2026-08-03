---
title: "Capstone: Bounded CSP Work Processor"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build the producer → bounded workers → collector pipeline in `code/`. It hands values through
channels, stops each stage on context cancellation, closes output after workers finish, and passes
`go test -race`.

## Test source

```go
package main

import (
  "context"
  "testing"
)

func TestProcess(t *testing.T) {
  got := process(context.Background(), []int{1, 2, 3}, 2)
  if len(got) != 3 {
    t.Fatalf("got %v", got)
  }
}
```
