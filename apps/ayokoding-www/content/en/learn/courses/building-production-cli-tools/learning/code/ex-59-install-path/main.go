package main

import (
	"fmt"
	"os"
)

func main() { fmt.Printf("install destination: %s/.local/bin\n", os.Getenv("HOME")) }
