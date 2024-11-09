"use strict";

const { RuleEngine, parseDuration } = require("../../src/rules/engine");
const { loadRules } = require("../../src/rules/loader");
const path = require("path");

describe("RuleEngine", () => {
  const channel = (sent) => ({
    name: "test",
    send: async (t) => sent.push(t),
  });

  it("fires when the metric exceeds the threshold", async () => {
    const sent = [];
    const engine = new RuleEngine(
      [
        {
          name: "high-latency",
          when: { metric: "rpc_latency_ms", operator: ">", value: 500 },
        },
      ],
      [channel(sent)]
    );
    await engine.handle({ rpc_latency_ms: 700 });
    expect(sent.length).toBe(1);
  });

  it("does not fire below the threshold", async () => {
    const sent = [];
    const engine = new RuleEngine(
      [
        {
          name: "high-latency",
          when: { metric: "rpc_latency_ms", operator: ">", value: 500 },
        },
      ],
      [channel(sent)]
    );
    await engine.handle({ rpc_latency_ms: 100 });
    expect(sent.length).toBe(0);
  });

  it("honors the for-duration window", async () => {
    const sent = [];
    const engine = new RuleEngine(
      [
        {
          name: "sustained",
          when: { metric: "load", operator: ">", value: 1, for: "1ms" },
        },
      ],
      [channel(sent)]
    );
    await engine.handle({ load: 5 });
    expect(sent.length).toBe(0);
    await new Promise((r) => setTimeout(r, 5));
    await engine.handle({ load: 5 });
    expect(sent.length).toBe(1);
  });

  it("resets state when the condition clears", async () => {
    const sent = [];
    const engine = new RuleEngine(
      [
        {
          name: "sustained",
          when: { metric: "load", operator: ">", value: 1, for: "1ms" },
        },
      ],
      [channel(sent)]
    );
    await engine.handle({ load: 5 });
    await engine.handle({ load: 0 }); // clears
    await new Promise((r) => setTimeout(r, 5));
    await engine.handle({ load: 5 });
    expect(sent.length).toBe(0);
  });
});

describe("parseDuration", () => {
  it("parses common durations", () => {
    expect(parseDuration("0s")).toBe(0);
    expect(parseDuration("60s")).toBe(60000);
    expect(parseDuration("5m")).toBe(300000);
    expect(parseDuration("1h")).toBe(3600000);
    expect(parseDuration("bogus")).toBe(0);
  });
});

describe("loadRules", () => {
  it("loads yaml rule files", () => {
    const rules = loadRules(path.join(__dirname, "../rules"));
    expect(Array.isArray(rules)).toBe(true);
    expect(rules.some((r) => r.name === "rpc-degradation")).toBe(true);
  });
});
