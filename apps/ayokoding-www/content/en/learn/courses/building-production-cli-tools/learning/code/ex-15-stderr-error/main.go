package main

import (
	"fmt"
	"os"
)

func main() { fmt.Fprintln(os.Stderr, "warning: cache is stale") }
