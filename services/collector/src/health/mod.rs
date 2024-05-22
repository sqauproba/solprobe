//! Health checks and readiness reporting for the collector.

use std::time::{Duration, Instant};

#[derive(Debug, Clone, PartialEq)]
pub enum Status {
    Healthy,
    Degraded(String),
}

impl Status {
    pub fn as_str(&self) -> &'static str {
        match self {
            Status::Healthy => "healthy",
            Status::Degraded(_) => "degraded",
        }
    }
}

/// Readiness: enforce the subscription cap and report degradation otherwise.
pub fn readiness(max_subscriptions: usize, active: usize) -> Status {
    if active > max_subscriptions {
        Status::Degraded(format!(
            "subscription count {active} exceeds limit {max_subscriptions}"
        ))
    } else {
        Status::Healthy
    }
}

/// Liveness tracker — last successful event receipt.
#[derive(Debug, Clone)]
pub struct Liveness {
    last_event: Option<Instant>,
    stale_after: Duration,
}

impl Liveness {
    pub fn new(stale_after: Duration) -> Self {
        Self {
            last_event: None,
            stale_after,
        }
    }

    pub fn record_event(&mut self) {
        self.last_event = Some(Instant::now());
    }

    pub fn is_stale(&self) -> bool {
        match self.last_event {
            Some(t) => t.elapsed() > self.stale_after,
            None => true,
        }
    }

    pub fn liveness_status(&self) -> Status {
        if self.is_stale() {
            Status::Degraded("no events received within staleness window".to_string())
        } else {
            Status::Healthy
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn readiness_flags_over_capacity() {
        assert_eq!(readiness(2, 1), Status::Healthy);
        assert!(matches!(readiness(2, 3), Status::Degraded(_)));
    }

    #[test]
    fn liveness_starts_stale() {
        let l = Liveness::new(Duration::from_secs(60));
        assert!(l.is_stale());
    }
}
