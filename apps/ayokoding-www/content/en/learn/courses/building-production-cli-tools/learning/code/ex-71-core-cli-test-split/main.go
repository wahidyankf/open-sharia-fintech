package main

import "fmt"

func normalize(region string) string {
	if region == "" {
		return "local"
	}
	return region
}

func main() {
	if normalize("") != "local" {
		panic("core test failed")
	}
	fmt.Println("status " + normalize("eu"))
}
