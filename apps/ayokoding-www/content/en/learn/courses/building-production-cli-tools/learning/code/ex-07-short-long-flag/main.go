package main

import (
	"flag"
	"fmt"
)

func main() {
	var verbose bool
	flag.BoolVar(&verbose, "verbose", false, "show detail")
	flag.BoolVar(&verbose, "v", false, "show detail")
	flag.Parse()
	fmt.Printf("verbose=%t\n", verbose)
}
