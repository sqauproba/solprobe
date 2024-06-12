//! Subscription lifecycle management.
//!
//! Tracks active subscriptions so the collector can enforce the configured
//! maximum and report counts for health checks and metrics.

use std::collections::HashSet;
use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Clone, Default)]
pub struct SubscriptionRegistry {
    active: Arc<Mutex<HashSet<String>>>,
    capacity: usize,
}

impl SubscriptionRegistry {
    pub fn new() -> Self {
        Self {
            active: Arc::new(Mutex::new(HashSet::new())),
            capacity: 500,
        }
    }

    pub fn with_capacity(capacity: usize) -> Self {
        Self {
            active: Arc::new(Mutex::new(HashSet::new())),
            capacity,
        }
    }

    pub async fn add(&self, key: String) -> bool {
        let mut active = self.active.lock().await;
        if active.len() >= self.capacity {
            return false;
        }
        active.insert(key)
    }

    pub async fn remove(&self, key: &str) -> bool {
        self.active.lock().await.remove(key)
    }

    pub async fn contains(&self, key: &str) -> bool {
        self.active.lock().await.contains(key)
    }

    pub async fn count(&self) -> usize {
        self.active.lock().await.len()
    }

    pub async fn capacity(&self) -> usize {
        self.capacity
    }

    pub async fn snapshot(&self) -> Vec<String> {
        self.active.lock().await.iter().cloned().collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[tokio::test]
    async fn enforces_capacity() {
        let reg = SubscriptionRegistry::with_capacity(2);
        assert!(reg.add("a".into()).await);
        assert!(reg.add("b".into()).await);
        assert!(!reg.add("c".into()).await);
        assert_eq!(reg.count().await, 2);
        assert!(reg.remove("a").await);
        assert!(reg.add("c".into()).await);
        assert_eq!(reg.count().await, 2);
    }

    #[tokio::test]
    async fn deduplicates_keys() {
        let reg = SubscriptionRegistry::new();
        assert!(reg.add("slot".into()).await);
        assert!(!reg.add("slot".into()).await);
        assert_eq!(reg.count().await, 1);
    }
}
