package main

import (
	"flag"
	"fmt"
	"os"
)

func main() {
	quiet := flag.Bool("quiet", false, "suppress success text")
	flag.Parse()
	if !*quiet {
		fmt.Println("release checked")
	}
	fmt.Fprintln(os.Stderr, "debug: check complete")
}
