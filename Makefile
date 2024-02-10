.PHONY: dev test-all lint-all build release proto seed

dev:
	./scripts/dev.sh

bootstrap:
	./scripts/bootstrap.sh

test-all:
	./scripts/test-all.sh

lint-all:
	./scripts/lint-all.sh

build:
	cd apps/cli && pip install -e ".[dev]"
	cd services/collector && cargo build
	cd services/api && go build ./...
	cd apps/dashboard && npm install

proto:
	./scripts/generate-proto.sh

seed:
	./scripts/seed-dev-data.sh

release:
	./scripts/release.sh
