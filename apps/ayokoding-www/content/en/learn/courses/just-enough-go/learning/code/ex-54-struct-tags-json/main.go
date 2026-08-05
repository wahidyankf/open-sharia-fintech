// => struct tags json: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => struct tags json: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => struct tags json: marks one deliberate step in the struct tags json example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"encoding/json"
	// => struct tags json: marks one deliberate step in the struct tags json example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => struct tags json: marks one deliberate step in the struct tags json example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => struct tags json: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Name   string `json:"name"`
	Secret string `json:"-"`
}

// => struct tags json: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	bytes, _ := json.Marshal(Release{Name: "ship", Secret: "hidden"})
	fmt.Println(string(bytes))
}
