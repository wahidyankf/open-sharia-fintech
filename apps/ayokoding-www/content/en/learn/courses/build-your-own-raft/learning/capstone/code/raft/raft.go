// Package raft is a small deterministic Raft teaching model.
package raft

import "sort"

type Role string

const (
	Follower  Role = "follower"
	Candidate Role = "candidate"
	Leader    Role = "leader"
)

type Entry struct {
	Term    int
	Command string
}
type Node struct {
	ID          string
	Term        int
	Role        Role
	VotedFor    string
	Log         []Entry
	CommitIndex int
	Applied     int
	State       map[string]string
}

func NewNode(id string) *Node {
	return &Node{ID: id, Role: Follower, State: map[string]string{}, CommitIndex: -1, Applied: -1}
}
func (n *Node) StartElection() { n.Term++; n.Role = Candidate; n.VotedFor = n.ID }
func (n *Node) BecomeLeader()  { n.Role = Leader }
func (n *Node) StepDown(term int) {
	if term > n.Term {
		n.Term = term
		n.VotedFor = ""
	}
	n.Role = Follower
}
func (n *Node) Append(command string) { n.Log = append(n.Log, Entry{Term: n.Term, Command: command}) }
func (n *Node) Apply() {
	for n.Applied < n.CommitIndex {
		n.Applied++
		e := n.Log[n.Applied]
		var k, v string
		for i, c := range e.Command {
			if c == '=' {
				k = e.Command[:i]
				v = e.Command[i+1:]
				break
			}
		}
		n.State[k] = v
	}
}

type Cluster struct {
	Nodes map[string]*Node
	Down  map[string]bool
}

func NewCluster(ids ...string) *Cluster {
	c := &Cluster{Nodes: map[string]*Node{}, Down: map[string]bool{}}
	for _, id := range ids {
		c.Nodes[id] = NewNode(id)
	}
	return c
}
func (c *Cluster) Elect(id string) bool {
	n := c.Nodes[id]
	if c.Down[id] {
		return false
	}
	n.StartElection()
	votes := 1
	for peer, p := range c.Nodes {
		if peer != id && !c.Down[peer] && p.Term <= n.Term {
			p.Term = n.Term
			p.VotedFor = id
			votes++
		}
	}
	if votes > len(c.Nodes)/2 {
		n.BecomeLeader()
		return true
	}
	return false
}
func (c *Cluster) Write(leader, command string) bool {
	l := c.Nodes[leader]
	if l.Role != Leader || c.Down[leader] {
		return false
	}
	l.Append(command)
	for id, n := range c.Nodes {
		if id != leader && !c.Down[id] {
			n.Term = l.Term
			n.Log = append([]Entry{}, l.Log...)
		}
	}
	count := 0
	for id, n := range c.Nodes {
		if !c.Down[id] && len(n.Log) == len(l.Log) {
			count++
		}
	}
	if count <= len(c.Nodes)/2 {
		return false
	}
	for _, n := range c.Nodes {
		if len(n.Log) == len(l.Log) {
			n.CommitIndex = len(l.Log) - 1
			n.Apply()
		}
	}
	return true
}
func (c *Cluster) Logs() []string {
	result := make([]string, 0, len(c.Nodes))
	for _, n := range c.Nodes {
		result = append(result, n.ID+":"+string(rune(len(n.Log))))
	}
	sort.Strings(result)
	return result
}
