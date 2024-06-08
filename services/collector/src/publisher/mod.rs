//! Publish normalized events to downstream services.
//!
//! In the full deployment this is a gRPC publisher (tonic + prost) fanning
//! events out to the API, analyzer, and alerts services. For the scaffold we
//! provide a stubbed publisher that logs events and batches them to a bounded
//! channel, which is what the real publisher will consume.

use std::sync::Arc;
use tokio::sync::mpsc;

use crate::decoders::Event;

const CHANNEL_CAPACITY: usize = 10_000;

#[derive(Clone)]
pub struct Publisher {
    tx: mpsc::Sender<Event>,
}

impl Publisher {
    /// Create a publisher and spawn a background consumer loop.
    pub fn new() -> Self {
        let (tx, mut rx) = mpsc::channel::<Event>(CHANNEL_CAPACITY);
        tokio::spawn(async move {
            let mut total: u64 = 0;
            while let Some(event) = rx.recv().await {
                total += 1;
                // Real impl: encode via prost and send over gRPC.
                tracing::debug!(total, "event queued for downstream publish");
            }
        });
        Self { tx }
    }

    pub async fn publish(&self, event: Event) -> anyhow::Result<()> {
        // Bounded channel applies backpressure instead of dropping events.
        self.tx
            .send(event)
            .await
            .map_err(|e| anyhow::anyhow!("publish channel closed: {e}"))
    }
}

impl Default for Publisher {
    fn default() -> Self {
        Self::new()
    }
}

/// Global publisher used by the run loop.
static PUBLISHER: std::sync::OnceLock<Arc<Publisher>> = std::sync::OnceLock::new();

pub async fn publish(event: Event) -> anyhow::Result<()> {
    let publisher = PUBLISHER
        .get_or_init(|| Arc::new(Publisher::new()))
        .clone();
    publisher.publish(event).await
}
