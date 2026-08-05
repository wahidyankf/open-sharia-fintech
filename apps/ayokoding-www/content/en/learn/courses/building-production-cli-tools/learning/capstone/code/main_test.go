package main

import (
	"os"
	"testing"
)

func TestRegionForFlagWins(t *testing.T) {
	t.Setenv("SHIP_REGION", "env")
	if got := regionFor("flag"); got != "flag" {
		t.Fatalf("got %q", got)
	}
}
func TestRegionForEnvWins(t *testing.T) {
	t.Setenv("SHIP_REGION", "env")
	if got := regionFor(""); got != "env" {
		t.Fatalf("got %q", got)
	}
}
func TestIsTerminalForRegularFile(t *testing.T) {
	path := t.TempDir() + "/out"
	if err := os.WriteFile(path, nil, 0o600); err != nil {
		t.Fatal(err)
	}
	handle, err := os.Open(path)
	if err != nil {
		t.Fatal(err)
	}
	defer handle.Close()
	if isTerminal(handle) {
		t.Fatal("regular file reported as terminal")
	}
}
