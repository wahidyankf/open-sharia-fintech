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
	chosen := strings.TrimSpace(string(readConfig()))
	if env := os.Getenv("SHIP_REGION"); env != "" {
		chosen = env
	}
	if *region != "" {
		chosen = *region
	}
	if chosen == "" {
		chosen = "local"
	}
	fmt.Println(chosen)
}
func readConfig() []byte { b, _ := os.ReadFile("ship.conf"); return b }
