# Docker build helpers

Per-service `Dockerfile`s live in each service directory. This folder holds
shared docker assets.

- `docker-compose.yml` — local full-stack stack (see repo root for the file)
- `infra/kubernetes/` — Kubernetes manifests
- `infra/terraform/` — Terraform modules
- `infra/helm/` — Helm charts
