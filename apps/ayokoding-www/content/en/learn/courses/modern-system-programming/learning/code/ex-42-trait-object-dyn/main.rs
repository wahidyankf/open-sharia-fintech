// co-18 trait-objects: dyn Trait chooses behavior via a vtable at runtime.
trait Describe {
    fn describe(&self) -> &'static str;
}
struct Disk;
impl Describe for Disk {
    fn describe(&self) -> &'static str {
        "disk"
    }
}
fn main() {
    let device: Box<dyn Describe> = Box::new(Disk);
    assert_eq!(device.describe(), "disk");
}
