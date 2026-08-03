package main

import (
	"flag"
	"fmt"
)

type count int

func (c *count) String() string   { return fmt.Sprint(*c) }
func (c *count) Set(string) error { *c++; return nil }
func main() {
	var verbose count
	flag.Var(&verbose, "v", "increase verbosity (repeatable)")
	flag.Parse()
	fmt.Printf("verbosity=%d\n", verbose)
}
