// &self reads a value; &mut self changes it.
// The caller selects the required access mode.
struct Counter(u32);
impl Counter {
    fn value(&self) -> u32 {
        self.0
    }
    fn increment(&mut self) {
        self.0 += 1;
    }
}
fn main() {
    let mut counter = Counter(0);
    counter.increment();
    println!("{}", counter.value());
}
