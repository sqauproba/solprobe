"use strict";

const fs = require("fs");
const path = require("path");
const YAML = require("yaml");

/**
 * Load all YAML rule files from a directory.
 *
 * Each file may contain either a single rule object or an array of rules.
 * Returns a flat array of normalized rules.
 */
function loadRules(dir) {
  const rules = [];
  for (const name of fs.readdirSync(dir)) {
    if (!name.endsWith(".yml") && !name.endsWith(".yaml")) continue;
    const full = path.join(dir, name);
    const raw = fs.readFileSync(full, "utf8");
    let doc;
    try {
      doc = YAML.parse(raw);
    } catch (err) {
      console.error(`solprobe-alerts: failed to parse ${name}: ${err.message}`);
      continue;
    }
    if (Array.isArray(doc)) {
      rules.push(...doc.map((r) => normalize(r, name)));
    } else if (doc && doc.name) {
      rules.push(normalize(doc, name));
    }
  }
  return rules;
}

function normalize(rule, source) {
  return {
    name: rule.name,
    source,
    when: {
      metric: rule.when?.metric,
      operator: rule.when?.operator || ">",
      value: rule.when?.value ?? 0,
      for: rule.when?.for || "0s",
    },
    notify: rule.notify || [],
    message: rule.message || null,
  };
}

module.exports = { loadRules };
