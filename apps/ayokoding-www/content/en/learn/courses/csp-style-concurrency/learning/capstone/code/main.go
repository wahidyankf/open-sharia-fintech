package main

import (
	"context"
	"fmt"
	"sync"
)

func process(ctx context.Context, jobs []int, workers int) []int {
	in, out := make(chan int), make(chan int)
	var wait sync.WaitGroup
	for i := 0; i < workers; i++ {
		wait.Add(1)
		go func() {
			defer wait.Done()
			for {
				select {
				case <-ctx.Done():
					return
				case job, ok := <-in:
					if !ok {
						return
					}
					select {
					case out <- job * job:
					case <-ctx.Done():
						return
					}
				}
			}
		}()
	}
	go func() {
		defer close(in)
		for _, job := range jobs {
			select {
			case in <- job:
			case <-ctx.Done():
				return
			}
		}
	}()
	go func() { wait.Wait(); close(out) }()
	result := []int{}
	for value := range out {
		result = append(result, value)
	}
	return result
}

func main() { fmt.Println(process(context.Background(), []int{1, 2, 3}, 2)) }
