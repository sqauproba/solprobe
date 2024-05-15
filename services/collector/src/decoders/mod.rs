//! Event decoding and normalization into typed messages.

use serde::Deserialize;

#[derive(Debug, Clone, Deserialize, PartialEq)]
pub struct SlotEvent {
    pub slot: u64,
    #[serde(default)]
    pub parent: Option<u64>,
    #[serde(default)]
    pub root: Option<u64>,
}

#[derive(Debug, Clone, Deserialize, PartialEq)]
pub struct LogEvent {
    pub signature: String,
    pub logs: Vec<String>,
    #[serde(default)]
    pub err: Option<serde_json::Value>,
}

#[derive(Debug, Clone, Deserialize, PartialEq)]
pub struct AccountEvent {
    pub address: String,
    pub owner: String,
    #[serde(default)]
    pub lamports: Option<u64>,
}

/// A normalized, typed event emitted by the collector.
#[derive(Debug, Clone, PartialEq)]
pub enum Event {
    Slot(SlotEvent),
    Log(LogEvent),
    Account(AccountEvent),
    Unknown(serde_json::Value),
}

/// Parse a raw WebSocket notification into a typed [`Event`].
///
/// Notifications carry the method that produced them (e.g.
/// ``slotNotification``); we match on that to route to the right decoder.
pub fn parse_notification(notification: &serde_json::Value) -> Option<Event> {
    let method = notification.get("method")?.as_str()?;
    let params = notification.get("params")?;
    let result = params.get("result")?;

    match method {
        "slotNotification" => serde_json::from_value::<SlotEvent>(result.clone())
            .ok()
            .map(Event::Slot),
        "logsNotification" => {
            let value = result.clone();
            // logsNotification returns an object with a nested value;
            // normalize common shapes defensively.
            let candidate = value
                .get("value")
                .cloned()
                .unwrap_or_else(|| value.clone());
            serde_json::from_value::<LogEvent>(candidate)
                .ok()
                .map(Event::Log)
        }
        "accountNotification" => {
            let value = result.get("value").cloned().unwrap_or_else(|| result.clone());
            let info = value.get("info").cloned().unwrap_or(value);
            Some(Event::Account(AccountEvent {
                address: notification
                    .get("params")
                    .and_then(|p| p.get("result"))
                    .and_then(|r| r.get("context"))
                    .and_then(|c| c.get("slot"))
                    .map(|s| s.to_string())
                    .unwrap_or_default(),
                owner: info
                    .get("owner")
                    .and_then(|o| o.as_str())
                    .unwrap_or_default()
                    .to_string(),
                lamports: info.get("lamports").and_then(|l| l.as_u64()),
            }))
        }
        _ => Some(Event::Unknown(notification.clone())),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn decodes_slot_notification() {
        let raw = serde_json::json!({
            "jsonrpc": "2.0",
            "method": "slotNotification",
            "params": { "result": { "slot": 12345, "parent": 12344, "root": 12300 } }
        });
        let event = parse_notification(&raw).expect("parses");
        match event {
            Event::Slot(s) => {
                assert_eq!(s.slot, 12345);
                assert_eq!(s.parent, Some(12344));
            }
            other => panic!("expected slot event, got {other:?}"),
        }
    }

    #[test]
    fn falls_back_to_unknown() {
        let raw = serde_json::json!({
            "method": "someCustomNotification",
            "params": { "result": { "x": 1 } }
        });
        assert!(matches!(
            parse_notification(&raw),
            Some(Event::Unknown(_))
        ));
    }
}
