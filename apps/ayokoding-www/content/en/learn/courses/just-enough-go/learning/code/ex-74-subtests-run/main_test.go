package main

import "testing"

func TestNamedCases(t *testing.T) {
	for _, name := range []string{"positive", "zero"} {
		t.Run(name, func(t *testing.T) { t.Log(name) })
	}
}
