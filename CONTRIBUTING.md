# Contributing to SolProbe

Thanks for your interest in contributing! SolProbe is an open-source Solana
observability platform built as a set of composable services. Every
contribution helps — code, docs, bug reports, and ideas are all welcome.

## Getting started

1. Fork the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make your changes in the relevant service directory.
4. Run that service's test suite (see the [Testing](#testing) section below).
5. Commit using [Conventional Commits](https://www.conventionalcommits.org/)
   (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`, `ci:`, `perf:`).
6. Open a Pull Request.

## Code of conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). Please be
kind, be constructive, and assume good faith.

## Where to make changes

- `apps/cli` — Python. Black + Ruff + Pytest.
- `services/collector` — Rust. `cargo fmt`, `clippy`, `cargo test`.
- `services/api` — Go. `gofmt`, `go vet`, `go test ./...`.
- `apps/dashboard` — TypeScript / Next.js. ESLint + `tsc --noEmit` + Vitest.
- `services/analyzer` — Python. Black + Ruff + Pytest.
- `services/alerts` — Node.js. ESLint + Jest.
- `proto/` — shared Protobuf contracts. Regenerate with
  `./scripts/generate-proto.sh` after editing.

## Testing

Run everything from the repo root:

```bash
make test-all
```

Or lint everything:

```bash
make lint-all
```

## Issues

Please open an issue to discuss significant changes before submitting a PR.
Use the issue templates provided under `.github/ISSUE_TEMPLATE/`.
