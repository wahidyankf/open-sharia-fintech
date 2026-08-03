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
