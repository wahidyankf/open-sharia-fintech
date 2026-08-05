// => json marshal unmarshal: declares the executable package boundary.
// => lets the Go tool recognize this as a runnable command.
package main

// => json marshal unmarshal: introduces only the standard-library dependency this slice needs.
// => keeps dependencies explicit so unused imports fail at compile time.
import (
	// => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"encoding/json"
	// => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
	// => keeps the mechanism inspectable before it is composed with another concern.
	"fmt"
	// => json marshal unmarshal: marks one deliberate step in the json marshal unmarshal example.
	// => keeps the mechanism inspectable before it is composed with another concern.
)

// => json marshal unmarshal: defines the type that carries this example’s data or contract.
// => makes the following operations statically checkable.
type Release struct {
	Name string `json:"name"`
}

// => json marshal unmarshal: names the behavior being demonstrated.
// => keeps the example callable from main or a test.
func main() {
	original := Release{Name: "ship"}
	bytes, _ := json.Marshal(original)
	var decoded Release
	json.Unmarshal(bytes, &decoded)
	fmt.Println(decoded == original)
}
