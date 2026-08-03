package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	region := strings.TrimSpace(string(must(os.ReadFile("ship.conf"))))
	if env := os.Getenv("SHIP_REGION"); env != "" {
		region = env
	}
	fmt.Println(region)
}
func must(b []byte, err error) []byte {
	if err != nil {
		return []byte("local")
	}
	return b
}
