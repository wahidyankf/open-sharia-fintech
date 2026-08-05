package main

import (
	"context"
	"errors"
	"fmt"
)

type Checker interface {
	Check(context.Context, string) (string, error)
}
type LocalChecker struct{}

func (LocalChecker) Check(ctx context.Context, name string) (string, error) {
	if name == "" {
		return "", errors.New("name is required")
	}
	select {
	case <-ctx.Done():
		return "", ctx.Err()
	default:
		return "ok:" + name, nil
	}
}
func run(ctx context.Context, checker Checker, name string) (string, error) {
	result := make(chan struct {
		value string
		err   error
	}, 1)
	go func() {
		value, err := checker.Check(ctx, name)
		result <- struct {
			value string
			err   error
		}{value, err}
	}()
	select {
	case result := <-result:
		return result.value, result.err
	case <-ctx.Done():
		return "", ctx.Err()
	}
}
func main() {
	value, err := run(context.Background(), LocalChecker{}, "ship")
	if err != nil {
		fmt.Println("error:", err)
		return
	}
	fmt.Println(value)
}
