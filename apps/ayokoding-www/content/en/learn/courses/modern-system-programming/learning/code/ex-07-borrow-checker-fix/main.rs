// co-05: consume the first borrow before asking for another one.
fn main() {
    let mut words = String::from("rust");
    let length = words.len();
    words.push('!');
    assert_eq!((length, words), (4, String::from("rust!")));
}
