package main

import (
	"flag"
	"fmt"
)

func main() {
	retries := flag.Int("retries", 3, "retry count")
	flag.Parse()
	fmt.Printf("retries=%d\n", *retries)
}
