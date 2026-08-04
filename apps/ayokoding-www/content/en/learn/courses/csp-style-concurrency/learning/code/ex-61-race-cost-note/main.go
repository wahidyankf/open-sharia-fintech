package main

// race cost note: this diagnostic keeps synchronization and cleanup observable.
import "fmt"

// race cost note: this diagnostic keeps synchronization and cleanup observable.
func main() {
	// race cost note: this diagnostic keeps synchronization and cleanup observable.
	fmt.Println("benchmark with: GO111MODULE=off go test -race -bench=BenchmarkMutexCounter -benchtime=1x")
}
