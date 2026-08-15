// A small trait states the behavior generic reporting needs.
trait Named {
    fn name(&self) -> &str;
}

// The struct owns the service configuration this program inspects.
#[derive(Debug)]
struct Service {
    name: String,
    port: Option<u16>,
}

// The trait implementation exposes the service name without moving it.
impl Named for Service {
    fn name(&self) -> &str {
        &self.name
    }
}

// This enum models all successful readiness states in this small program.
#[derive(Debug, PartialEq)]
enum Readiness {
    Ready(u16),
}

// This enum models the recoverable configuration failure.
#[derive(Debug, PartialEq)]
enum ServiceError {
    MissingPort,
}

// ? turns a missing Option value into this function's Result error.
fn readiness(service: &Service) -> Result<Readiness, ServiceError> {
    let port = service.port.ok_or(ServiceError::MissingPort)?;
    Ok(Readiness::Ready(port))
}

// The generic requires only a readable name from its input.
fn report<T: Named>(service: &T, state: Readiness) -> String {
    match state {
        Readiness::Ready(port) => format!("{} is ready on {port}", service.name()),
    }
}

// ? propagates readiness failure to the caller without a panic.
fn run(service: &Service) -> Result<String, ServiceError> {
    Ok(report(service, readiness(service)?))
}

fn main() {
    let service = Service {
        name: "api".into(),
        port: Some(443),
    };
    match run(&service) {
        Ok(line) => println!("{line}"),
        Err(ServiceError::MissingPort) => println!("api is missing a port"),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn reports_a_ready_service() {
        let service = Service {
            name: "api".into(),
            port: Some(443),
        };
        assert_eq!(run(&service), Ok("api is ready on 443".into()));
    }

    #[test]
    fn rejects_a_missing_port() {
        let service = Service {
            name: "api".into(),
            port: None,
        };
        assert_eq!(run(&service), Err(ServiceError::MissingPort));
    }
}
