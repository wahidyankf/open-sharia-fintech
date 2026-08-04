package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 3 || os.Args[2] != "--help" {
		fmt.Fprintln(os.Stderr, "usage: ship COMMAND --help")
		os.Exit(2)
	}
	switch os.Args[1] {
	case "check":
		fmt.Println("usage: ship check FILE")
	case "publish":
		fmt.Println("usage: ship publish RELEASE")
	default:
		fmt.Fprintln(os.Stderr, "unknown command")
		os.Exit(2)
	}
}
