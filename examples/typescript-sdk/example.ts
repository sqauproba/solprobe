# TypeScript SDK example

```bash
npm install @solprobe/sdk
```

```ts
import { SolProbeClient } from "@solprobe/sdk";

const client = new SolProbeClient("http://localhost:8080");

const health = await client.health();
console.log(`status: ${health.status} score: ${health.score}`);

const slot = await client.latestSlot();
console.log(`latest slot: ${slot.slot}`);
```
