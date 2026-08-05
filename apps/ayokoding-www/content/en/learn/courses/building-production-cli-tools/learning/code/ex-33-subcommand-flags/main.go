package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 || os.Args[1] != "publish" {
		fmt.Fprintln(os.Stderr, "usage: ship publish --dry-run")
		os.Exit(2)
	}
	fs := flag.NewFlagSet("publish", flag.ExitOnError)
	dry := fs.Bool("dry-run", false, "do not publish")
	fs.Parse(os.Args[2:])
	fmt.Printf("dry-run=%t\n", *dry)
}
