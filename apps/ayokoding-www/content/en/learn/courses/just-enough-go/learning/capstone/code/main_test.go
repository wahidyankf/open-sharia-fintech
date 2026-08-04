package main

import (
	"context"
	"testing"
)

func TestRun(t *testing.T) {
	got, err := run(context.Background(), LocalChecker{}, "ship")
	if err != nil || got != "ok:ship" {
		t.Fatalf("got %q, err %v", got, err)
	}
}
