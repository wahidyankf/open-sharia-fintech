//! Step 3: generic iterator code is monomorphized for each concrete input type.

pub trait Bytes {
    fn value(self) -> u32;
}
impl Bytes for u8 {
    fn value(self) -> u32 {
        self.into()
    }
}

pub fn sum<I, T>(items: I) -> u32
where
    I: IntoIterator<Item = T>,
    T: Bytes,
{
    items.into_iter().map(Bytes::value).sum()
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn preserves_behavior() {
        assert_eq!(sum([20_u8, 22]), 42);
    }
}
