package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	data, err := os.ReadFile("ship.conf")
	if err != nil {
		fmt.Println("region=local")
		return
	}
	fmt.Println(strings.TrimSpace(string(data)))
}
