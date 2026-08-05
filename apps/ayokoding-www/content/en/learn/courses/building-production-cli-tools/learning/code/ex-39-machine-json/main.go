package main

import (
	"encoding/json"
	"os"
)

func main() {
	// => JSON is written only to stdout so jq and other callers can parse it.
	// => A stable key is a public script contract.
	json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ok", "example": "39"})
}
