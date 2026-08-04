package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintln(os.Stderr, "usage: ship <check|publish>")
		os.Exit(2)
	}
	switch os.Args[1] {
	case "check":
		fmt.Println("ok")
	case "publish":
		fmt.Println("published")
	default:
		fmt.Fprintln(os.Stderr, "unknown command; run --help")
		os.Exit(2)
	}
}
