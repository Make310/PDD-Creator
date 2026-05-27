.PHONY: setup checks test test-unit test-integration test-acceptance

setup:
	bash scripts/local-setup.sh

checks:
	@[ -f api/Makefile ] && (cd api && make checks) || echo "api/ not scaffolded yet"
	@[ -f worker/Makefile ] && (cd worker && make checks) || echo "worker/ not scaffolded yet"

test-unit:
	@[ -f api/Makefile ] && (cd api && make test-unit) || echo "api/ not scaffolded yet"
	@[ -f worker/Makefile ] && (cd worker && make test-unit) || echo "worker/ not scaffolded yet"

test-integration:
	@[ -f api/Makefile ] && (cd api && make test-integration) || echo "api/ not scaffolded yet"
	@[ -f worker/Makefile ] && (cd worker && make test-integration) || echo "worker/ not scaffolded yet"

test-acceptance:
	@[ -f api/Makefile ] && (cd api && make test-acceptance) || echo "api/ not scaffolded yet"
	@[ -f worker/Makefile ] && (cd worker && make test-acceptance) || echo "worker/ not scaffolded yet"

test:
	@[ -f api/Makefile ] && (cd api && make test) || echo "api/ not scaffolded yet"
	@[ -f worker/Makefile ] && (cd worker && make test) || echo "worker/ not scaffolded yet"
