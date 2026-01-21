# Security Policy

## Supported versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a vulnerability

We take security seriously. Please do **not** open a public issue for
vulnerabilities.

Report privately by emailing `security@solprobe.dev` with:

- A description of the vulnerability.
- Steps to reproduce.
- The affected version(s) and component(s) (CLI, collector, api, etc.).
- Any suggested fix, if you have one.

We will acknowledge receipt within 48 hours and aim to triage within 7 days.
We follow responsible disclosure: please give us time to fix and release a
patched version before making details public.

## What is in scope

- Authentication and authorization (API keys, JWT).
- Input validation at API and CLI boundaries.
- Secrets handling (never commit keys, seed phrases, or tokens).
- Dependency supply-chain issues.

## Notes for operators

Never place these values in Git:

```text
PRIVATE_KEY
SEED_PHRASE
JWT_SECRET
DATABASE_PASSWORD
TELEGRAM_BOT_TOKEN
PROVIDER_API_KEY
```
