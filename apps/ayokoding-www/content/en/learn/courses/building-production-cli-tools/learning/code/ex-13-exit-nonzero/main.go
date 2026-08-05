package main

import (
	"fmt"
	"os"
)

func main() { fmt.Fprintln(os.Stderr, "error: remote is unavailable"); os.Exit(1) }
