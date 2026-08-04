package main

import (
	"flag"
	"fmt"
)

func main() {
	flag.Usage = func() { fmt.Fprintln(flag.CommandLine.Output(), "usage: ship [--dry-run] RELEASE") }
	dry := flag.Bool("dry-run", false, "print without publishing")
	flag.Parse()
	if flag.NArg() == 0 {
		flag.Usage()
		return
	}
	fmt.Printf("publish %s (dry-run=%t)\n", flag.Arg(0), *dry)
}
