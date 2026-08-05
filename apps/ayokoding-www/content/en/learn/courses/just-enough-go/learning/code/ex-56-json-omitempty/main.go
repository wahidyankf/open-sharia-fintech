// => json omitempty: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => json omitempty: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => json omitempty: marks one deliberate step in the json omitempty example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"encoding/json"
	// => json omitempty: marks one deliberate step in the json omitempty example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => json omitempty: marks one deliberate step in the json omitempty example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => json omitempty: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Name string `json:"name,omitempty"`
}

// => json omitempty: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() { bytes, _ := json.Marshal(Release{}); fmt.Println(string(bytes)) }
