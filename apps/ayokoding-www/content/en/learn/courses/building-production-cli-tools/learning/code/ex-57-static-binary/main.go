package main

import "fmt"

func main() { fmt.Println("CGO_ENABLED=0 go build -trimpath -o ship main.go") }
