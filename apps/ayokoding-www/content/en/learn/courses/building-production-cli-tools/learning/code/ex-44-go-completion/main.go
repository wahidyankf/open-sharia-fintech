package main

import (
	"fmt"
	"os"
)

func main() {
	if len(os.Args) == 3 && os.Args[1] == "completion" && os.Args[2] == "bash" {
		fmt.Println("complete -W 'check publish version' ship")
		return
	}
	fmt.Fprintln(os.Stderr, "usage: ship completion bash")
}
