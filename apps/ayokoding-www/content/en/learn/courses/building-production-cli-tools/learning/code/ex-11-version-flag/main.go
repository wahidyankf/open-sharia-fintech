package main

import (
	"flag"
	"fmt"
)

func main() {
	version := flag.Bool("version", false, "print version")
	flag.Parse()
	if *version {
		fmt.Println("ship 1.2.0")
		return
	}
	fmt.Println("run ship --version")
}
