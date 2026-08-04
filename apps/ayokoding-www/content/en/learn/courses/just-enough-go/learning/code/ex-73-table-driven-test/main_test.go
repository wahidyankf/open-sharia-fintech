package main

import "testing"

func TestDoubleCases(t *testing.T) {
	for _, test := range []struct{ in, want int }{{2, 4}, {3, 6}} {
		if got := double(test.in); got != test.want {
			t.Fatalf("double(%d) = %d", test.in, got)
		}
	}
}
