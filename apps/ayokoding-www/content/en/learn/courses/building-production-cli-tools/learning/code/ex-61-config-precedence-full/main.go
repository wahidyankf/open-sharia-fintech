package main

import (
	"flag"
	"fmt"
	"os"
	"strings"
)

func main() {
	region := flag.String("region", "", "region")
	flag.Parse()
	value := strings.TrimSpace(string(read()))
	if env := os.Getenv("SHIP_REGION"); env != "" {
		value = env
	}
	if *region != "" {
		value = *region
	}
	if value == "" {
		value = "local"
	}
	fmt.Println(value)
}
func read() []byte { b, _ := os.ReadFile("ship.conf"); return b }
