package main

import (
	"fmt"
	"os"
)

func main() {
	switch os.Args[len(os.Args)-1] {
	case "ok":
		fmt.Println("ok")
	case "invalid":
		fmt.Fprintln(os.Stderr, "invalid input")
		os.Exit(2)
	default:
		fmt.Fprintln(os.Stderr, "operation failed")
		os.Exit(1)
	}
}
