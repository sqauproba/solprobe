//! Integration tests for the collector modules.

use std::time::Duration;

use solprobe_collector::decoders::{parse_notification, Event};
use solprobe_collector::health::{readiness, Liveness, Status};
use solprobe_collector::metrics::Metrics;
use solprobe_collector::subscriptions::SubscriptionRegistry;

#[test]
fn decodes_slot_notification() {
    let raw = serde_json::json!({
        "jsonrpc": "2.0",
        "method": "slotNotification",
        "params": { "result": { "slot": 9001, "parent": 9000, "root": 8990 } }
    });
    match parse_notification(&raw) {
        Some(Event::Slot(s)) => {
            assert_eq!(s.slot, 9001);
            assert_eq!(s.parent, Some(9000));
        }
        _ => panic!("expected slot event"),
    }
}

#[test]
fn readiness_obeys_capacity() {
    assert_eq!(readiness(500, 10), Status::Healthy);
    assert!(matches!(readiness(500, 501), Status::Degraded(_)));
}

#[test]
fn liveness_flags_staleness() {
    let mut liveness = Liveness::new(Duration::from_secs(1));
    assert!(liveness.is_stale());
    liveness.record_event();
    assert!(!liveness.is_stale());
}

#[test]
fn metrics_render_prometheus_format() {
    let m = Metrics::new();
    m.record_event();
    m.record_reconnect();
    let out = m.render_prometheus();
    assert!(out.contains("solprobe_events_ingested_total 1"));
    assert!(out.contains("solprobe_websocket_reconnects_total 1"));
}

#[tokio::test]
async fn registry_tracks_and_enforces_capacity() {
    let reg = SubscriptionRegistry::with_capacity(2);
    assert!(reg.add("account:x".into()).await);
    assert!(reg.add("account:y".into()).await);
    assert!(!reg.add("account:z".into()).await);
    assert_eq!(reg.count().await, 2);
    assert!(reg.contains("account:x").await);
    assert!(reg.remove("account:x").await);
    assert!(!reg.contains("account:x").await);
}
