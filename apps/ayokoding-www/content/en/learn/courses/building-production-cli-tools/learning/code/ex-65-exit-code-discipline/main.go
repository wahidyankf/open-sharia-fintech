package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: consumer <0|1|2>")
		os.Exit(2)
	}
	switch os.Args[1] {
	case "0":
		fmt.Println("continue pipeline")
	case "1":
		fmt.Println("retry operation")
	case "2":
		fmt.Println("fix command usage")
	default:
		os.Exit(2)
	}
}
