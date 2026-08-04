package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"os"
)

func main() {
	machine := flag.Bool("json", false, "machine output")
	flag.Parse()
	if *machine {
		_ = json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ready"})
		return
	}
	fmt.Println("release ready")
}
