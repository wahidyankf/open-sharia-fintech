package main

import (
	"flag"
	"fmt"
)

func main() {
	verbose := flag.Bool("verbose", false, "show detail")
	flag.Parse()
	fmt.Printf("verbose=%t\n", *verbose)
}
