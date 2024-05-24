//! Prometheus-compatible metrics emission.
//!
//! Collectors expose counters/gauges that are exported on the metrics
//! endpoint in the Prometheus text exposition format.

use std::collections::BTreeMap;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::Arc;

#[derive(Clone, Default)]
pub struct Metrics {
    events_ingested: Arc<AtomicU64>,
    ws_reconnects: Arc<AtomicU64>,
    active_subscriptions: Arc<AtomicU64>,
}

impl Metrics {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn record_event(&self) {
        self.events_ingested.fetch_add(1, Ordering::Relaxed);
    }

    pub fn record_reconnect(&self) {
        self.ws_reconnects.fetch_add(1, Ordering::Relaxed);
    }

    pub fn set_active_subscriptions(&self, count: u64) {
        self.active_subscriptions.store(count, Ordering::Relaxed);
    }

    pub fn events_ingested(&self) -> u64 {
        self.events_ingested.load(Ordering::Relaxed)
    }

    pub fn reconnects(&self) -> u64 {
        self.ws_reconnects.load(Ordering::Relaxed)
    }

    pub fn active_subscriptions(&self) -> u64 {
        self.active_subscriptions.load(Ordering::Relaxed)
    }

    /// Render metrics in the Prometheus text exposition format.
    pub fn render_prometheus(&self) -> String {
        let mut lines: BTreeMap<String, String> = BTreeMap::new();
        lines.insert(
            "solprobe_events_ingested_total".to_string(),
            format!("{}", self.events_ingested()),
        );
        lines.insert(
            "solprobe_websocket_reconnects_total".to_string(),
            format!("{}", self.reconnects()),
        );
        lines.insert(
            "solprobe_active_subscriptions".to_string(),
            format!("{}", self.active_subscriptions()),
        );

        let mut out = String::new();
        out.push_str("# TYPE solprobe_events_ingested_total counter\n");
        out.push_str(&format!(
            "solprobe_events_ingested_total {}\n",
            self.events_ingested()
        ));
        out.push_str("# TYPE solprobe_websocket_reconnects_total counter\n");
        out.push_str(&format!(
            "solprobe_websocket_reconnects_total {}\n",
            self.reconnects()
        ));
        out.push_str("# TYPE solprobe_active_subscriptions gauge\n");
        out.push_str(&format!(
            "solprobe_active_subscriptions {}\n",
            self.active_subscriptions()
        ));
        let _ = lines;
        out
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn records_and_renders_metrics() {
        let m = Metrics::new();
        m.record_event();
        m.record_event();
        m.record_reconnect();
        m.set_active_subscriptions(3);
        assert_eq!(m.events_ingested(), 2);
        assert_eq!(m.reconnects(), 1);
        let rendered = m.render_prometheus();
        assert!(rendered.contains("solprobe_events_ingested_total 2"));
        assert!(rendered.contains("solprobe_active_subscriptions 3"));
    }
}
