# SolProbe CLI

The primary developer interface for SolProbe — fast, terminal-first diagnostics
for the Solana network. Built with Typer, Rich, and Textual.

## Install

```bash
cd apps/cli
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
solprobe --help
```

Requires Python `>= 3.11`.

## Commands

```bash
solprobe status
solprobe network health
solprobe rpc benchmark
solprobe rpc compare
solprobe slots latest
solprobe slots watch
solprobe fees
solprobe wallet inspect <ADDRESS>
solprobe wallet watch <ADDRESS>
solprobe program inspect <PROGRAM_ID>
solprobe program logs <PROGRAM_ID>
solprobe tx inspect <SIGNATURE>
solprobe tx simulate <FILE>
solprobe tui
```

## Configuration

Reads configuration from environment variables (see root `.env.example`) with
sensible defaults for the public RPC endpoint.
