"use strict";

/**
 * Matches incoming events against declarative rules and dispatches to
 * notification channels.
 *
 * Supports threshold conditions (>, <, >=, <=, ==) plus an optional
 * `for` duration that requires the condition to persist across samples
 * before firing.
 */
class RuleEngine {
  constructor(rules, channels) {
    this.rules = rules;
    this.channels = channels;
    this.state = new Map(); // ruleName -> { since, last }
  }

  /** Evaluate an event against every rule; dispatch for those that fire. */
  async handle(event) {
    for (const rule of this.rules) {
      const matched = this.matches(rule, event);
      if (matched) {
        await this.fire(rule, event);
      } else {
        this.state.delete(rule.name);
      }
    }
  }

  matches(rule, event) {
    const { when } = rule;
    const value = event[when.metric];
    if (value === undefined) return false;

    let hit = false;
    switch (when.operator) {
      case ">":
        hit = value > when.value;
        break;
      case "<":
        hit = value < when.value;
        break;
      case ">=":
        hit = value >= when.value;
        break;
      case "<=":
        hit = value <= when.value;
        break;
      case "==":
        hit = value === when.value;
        break;
      default:
        return false;
    }
    return hit;
  }

  /**
   * Decide whether a rule should fire, honoring the `for` window: the
   * condition must persist for the configured duration before we alert.
   */
  shouldFire(rule, event) {
    const now = Date.now();
    const reqMs = parseDuration(rule.when.for);

    const st = this.state.get(rule.name);
    if (reqMs <= 0) {
      return true;
    }
    if (!st) {
      this.state.set(rule.name, { since: now });
      return false;
    }
    if (now - st.since >= reqMs) {
      return true;
    }
    return false;
  }

  async fire(rule, event) {
    if (!this.shouldFire(rule, event)) return;
    const value = event[rule.when.metric];
    const text =
      rule.message ||
      `[${rule.name}] ${rule.when.metric} ${rule.when.operator} ${rule.when.value} (now ${value})`;
    const selected = this.channels.filter(
      (c) =>
        !rule.notify ||
        rule.notify.length === 0 ||
        rule.notify.includes(c.name)
    );
    for (const channel of selected) {
      try {
        await channel.send(text, event);
      } catch (err) {
        console.error(`solprobe-alerts: channel ${channel.name} failed: ${err.message}`);
      }
    }
  }

  async stop() {
    this.state.clear();
  }
}

/** Parse a Go-style duration string ("60s", "5m", "1h") into milliseconds. */
function parseDuration(input) {
  if (typeof input !== "string") return 0;
  const m = /^(\d+)(ms|s|m|h)$/.exec(input.trim());
  if (!m) return 0;
  const n = Number(m[1]);
  switch (m[2]) {
    case "ms":
      return n;
    case "s":
      return n * 1000;
    case "m":
      return n * 60 * 1000;
    case "h":
      return n * 60 * 60 * 1000;
    default:
      return 0;
  }
}

module.exports = { RuleEngine, parseDuration };
