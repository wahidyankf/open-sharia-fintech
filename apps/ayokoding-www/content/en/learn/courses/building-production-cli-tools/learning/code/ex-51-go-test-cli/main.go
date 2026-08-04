package main

import (
	"fmt"
	"os"
)

func run(args []string) (string, int) {
	if len(args) != 1 {
		return "usage: ship RELEASE", 2
	}
	return "published " + args[0], 0
}

func main() {
	output, code := run(os.Args[1:])
	if len(os.Args) == 1 {
		output, code = run([]string{"v1"})
	}
	if output != "published v1" || code != 0 {
		panic("CLI contract changed")
	}
	fmt.Println(output)
}
