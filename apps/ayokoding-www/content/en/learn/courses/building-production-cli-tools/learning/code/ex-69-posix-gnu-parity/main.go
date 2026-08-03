package main

import (
	"fmt"
	"os"
)

func main() {
	for _, a := range os.Args[1:] {
		if a == "-v" || a == "--verbose" {
			fmt.Println("verbose=true")
			return
		}
	}
	fmt.Println("verbose=false")
}
