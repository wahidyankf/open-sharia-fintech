package main

import (
	"fmt"
	"os"
)

func main() { fmt.Fprintln(os.Stderr, "error: release not found"); os.Exit(1) }
