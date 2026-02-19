# Deployment

SolProbe can be deployed several ways.

## Docker Compose

For local/staging:

```bash
docker compose -f infra/docker-compose.yml up --build
```

## Kubernetes

Apply the manifests in `infra/kubernetes/`:

```bash
kubectl apply -f infra/kubernetes/
```

## Terraform

Provision managed Postgres and Redis (see `infra/terraform/`), then deploy the
services against them.

## Helm

Use the chart in `infra/helm/` for repeatable cluster deployments.

## CI/CD

GitHub Actions workflows in `.github/workflows/` build, test, and publish
container images on tagged releases.
