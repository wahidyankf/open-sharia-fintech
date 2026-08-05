package main

import (
	"fmt"
	"os"
)

func main() {
	info, err := os.Stdout.Stat()
	if err != nil {
		panic(err)
	}
	fmt.Printf("interactive=%t\n", info.Mode()&os.ModeCharDevice != 0)
}
