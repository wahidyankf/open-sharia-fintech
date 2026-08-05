package main

import (
	"fmt"
	"os"
)

func main() {
	if err := os.WriteFile("/missing/path", nil, 0o600); err != nil {
		fmt.Println(err)
	}
}
