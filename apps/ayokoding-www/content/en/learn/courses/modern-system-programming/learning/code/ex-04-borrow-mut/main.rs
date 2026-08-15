// co-04 borrow-mut: one exclusive reference may change its referent.
fn main() {
    let mut value = String::from("safe");
    {
        let edit = &mut value;
        edit.push_str("ly");
    }
    assert_eq!(value, "safely");
}
