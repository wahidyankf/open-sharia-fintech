package main

import "fmt"

// render is the policy-free core a unit test can call without a terminal.
func render(name string) string { return "hello " + name }

func main() {
	// => Argument parsing and process concerns stay outside the core.
	fmt.Println(render("ship"))
}
