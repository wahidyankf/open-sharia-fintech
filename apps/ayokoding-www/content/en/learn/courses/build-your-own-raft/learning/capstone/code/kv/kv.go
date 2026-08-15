// Package kv exposes the state-machine view of a Raft node.
package kv

import "example.com/raftkv/raft"

func Get(node *raft.Node, key string) (string, bool) { value, ok := node.State[key]; return value, ok }
