package main

import (
	"fmt"
	"os"
)

func main() {
	token := os.Getenv("SHIP_TOKEN")
	if token == "" {
		fmt.Fprintln(os.Stderr, "SHIP_TOKEN is required")
		os.Exit(2)
	}
	fmt.Printf("token supplied (%d bytes)\n", len(token))
}
