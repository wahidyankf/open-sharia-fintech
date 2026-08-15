// A closure is a value that can be passed as an argument.
// apply invokes the supplied behavior once.
fn apply<F: Fn(i32) -> i32>(operation: F, value: i32) -> i32 {
    operation(value)
}
fn main() {
    println!("{}", apply(|value| value + 1, 41));
}
