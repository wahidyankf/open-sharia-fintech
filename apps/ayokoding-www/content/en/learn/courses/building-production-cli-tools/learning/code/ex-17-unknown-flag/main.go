package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	flag.Usage = func() { fmt.Fprintln(os.Stderr, "usage: ship [--dry-run]") }
	flag.Parse()
	fmt.Println("arguments accepted")
}
