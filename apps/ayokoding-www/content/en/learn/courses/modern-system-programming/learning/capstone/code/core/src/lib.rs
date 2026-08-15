//! Step 1: the core owns input and exposes errors as values.

#[derive(Debug, PartialEq, Eq)]
pub enum CoreError {
    Empty,
}

pub fn first_byte(bytes: Vec<u8>) -> Result<u8, CoreError> {
    bytes.into_iter().next().ok_or(CoreError::Empty)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn accepts_owned_input() {
        assert_eq!(first_byte(vec![42]), Ok(42));
    }
    #[test]
    fn reports_empty() {
        assert_eq!(first_byte(vec![]), Err(CoreError::Empty));
    }
}
