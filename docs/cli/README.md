# CLI reference

`solprobe` is a terminal-first Solana diagnostics tool.

## Global options

| Option | Description |
|---|---|
| `--version` / `-V` | Print version and exit |
| `--endpoint` / `-e` | Override the RPC endpoint |
| `--verbose` / `-v` | Enable debug logging |

## Commands

| Command | Description |
|---|---|
| `solprobe status` | Network overview |
| `solprobe config` | Show resolved configuration |
| `solprobe network health` | Health score |
| `solprobe network overview` | Supply/validators/performance |
| `solprobe network performance` | Live performance monitor |
| `solprobe rpc benchmark` | Benchmark an endpoint |
| `solprobe rpc compare` | Compare endpoints |
| `solprobe rpc methods` | List benchmarked methods |
| `solprobe slots latest` | Latest slot info |
| `solprobe slots leaders` | Upcoming slot leaders |
| `solprobe slots watch` | Live slot stream |
| `solprobe fees` | Fee market |
| `solprobe fees estimate` | Fee estimate |
| `solprobe wallet inspect` | Wallet balances + activity |
| `solprobe wallet tokens` | SPL token accounts |
| `solprobe wallet watch` | Live balance monitor |
| `solprobe program inspect` | Program metadata |
| `solprobe program accounts` | Accounts owned by a program |
| `solprobe program logs` | Recent invocations + logs |
| `solprobe tx inspect` | Transaction details |
| `solprobe tx simulate` | Simulate a transaction |
| `solprobe tui` | Full-screen terminal UI |
