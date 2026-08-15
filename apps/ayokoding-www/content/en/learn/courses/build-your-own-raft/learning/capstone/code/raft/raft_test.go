package raft_test

import (
	"example.com/raftkv/kv"
	"example.com/raftkv/raft"
	"testing"
)

func TestElectionReplicationAndPartition(t *testing.T) {
	c := raft.NewCluster("a", "b", "c")
	if !c.Elect("a") {
		t.Fatal("expected majority election")
	}
	if !c.Write("a", "color=green") {
		t.Fatal("expected majority commit")
	}
	for _, id := range []string{"a", "b", "c"} {
		if got, ok := kv.Get(c.Nodes[id], "color"); !ok || got != "green" {
			t.Fatalf("%s has %q", id, got)
		}
	}
	c.Down["b"] = true
	c.Down["c"] = true
	if c.Write("a", "color=blue") {
		t.Fatal("minority must not commit")
	}
	c.Nodes["a"].StepDown(2)
	if c.Nodes["a"].Role != raft.Follower {
		t.Fatal("higher term must step down")
	}
}
func TestRestartStateCanRejoin(t *testing.T) {
	c := raft.NewCluster("a", "b", "c")
	if !c.Elect("a") || !c.Write("a", "n=1") {
		t.Fatal("setup failed")
	}
	restarted := raft.NewNode("b")
	restarted.Term = c.Nodes["b"].Term
	restarted.Log = append(restarted.Log, c.Nodes["b"].Log...)
	restarted.CommitIndex = c.Nodes["b"].CommitIndex
	restarted.Apply()
	if got, ok := kv.Get(restarted, "n"); !ok || got != "1" {
		t.Fatalf("restart lost state: %q", got)
	}
}
