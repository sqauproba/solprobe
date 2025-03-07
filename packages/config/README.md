# Shared configuration

Shared service configuration values, loaded by all services.

```yaml
solana:
  cluster: mainnet-beta
  rpc_endpoint: https://api.mainnet-beta.solana.com
  ws_endpoint: wss://api.mainnet-beta.solana.com/

storage:
  database_url: postgres://solprobe:solprobe@postgres:5432/solprobe
  redis_url: redis://redis:6379
```
