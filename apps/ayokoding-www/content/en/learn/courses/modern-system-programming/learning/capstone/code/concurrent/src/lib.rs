//! Step 2: channels transfer job ownership; Arc<Mutex<_>> protects the aggregate.

use std::sync::{Arc, Mutex, mpsc};

pub fn sum_jobs(jobs: Vec<u32>) -> u32 {
    let total = Arc::new(Mutex::new(0));
    let (tx, rx) = mpsc::channel();
    let worker_total = Arc::clone(&total);
    let worker = std::thread::spawn(move || {
        for job in rx {
            *worker_total.lock().expect("not poisoned") += job;
        }
    });
    for job in jobs {
        tx.send(job).expect("worker is alive");
    }
    drop(tx);
    worker.join().expect("worker completes");
    *total.lock().expect("not poisoned")
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn sums_race_free() {
        for _ in 0..20 {
            assert_eq!(sum_jobs(vec![20, 22]), 42);
        }
    }
}
