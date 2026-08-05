package main

import (
	"fmt"
	"os"
)

func main() {
	region := "local"
	if len(os.Args) > 1 {
		region = os.Args[1]
	}
	fmt.Printf("{\"region\":\"%s\",\"status\":\"ready\"}\n", region)
}
