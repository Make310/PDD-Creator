.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install python and the app packages
	uv python install 3.12.8
	uv python pin 3.12.8
	uv sync

.PHONY: update
update: ## Update the app packages
	uv lock --upgrade

.PHONY: add-package
add-package: ## Install a new package. ex: make add-package package=XXX
	uv add $(package)

.PHONY: add-dev-package
add-dev-package: ## Install a new dev package. ex: make add-dev-package package=XXX
	uv add --dev $(package)

.PHONY: run
run: ## Run the app in production mode
	OPENAPI_URL= uv run fastapi run

.PHONY: dev
dev: ## Run the app in development mode
	uv run fastapi dev

.PHONY: create-admin
create-admin: ## Create the first admin user. ex: make create-admin email=admin@x.com name="Admin" (password prompted or via ADMIN_PASSWORD)
	uv run python -m src.delivery.cli.create_admin --email "$(email)" --name "$(name)"

.PHONY: build
build: ## Build the docker image
	docker build -t pdd-creator-api .

.PHONY: up
up: build ## Run the app inside docker
	docker run -p 8000:8000 pdd-creator-api

.PHONY: check-typing
check-typing: ## Run the static type checker
	uv run ty check .

.PHONY: check-lint
check-lint: ## Check the code style
	uv run ruff check

.PHONY: lint
lint: ## Fix lint issues
	uv run ruff check --fix

.PHONY: check-format
check-format: ## Check the code format
	uv run ruff format --check

.PHONY: format
format: ## Format the code
	uv run ruff format

.PHONY: checks
checks: check-lint check-format check-typing ## Run all checks

.PHONY: test-unit
test-unit: ## Run unit tests
	uv run pytest tests/unit -ra -x --durations=5

.PHONY: test-integration
test-integration: ## Run integration tests (requires real services)
	@if [ -d tests/integration ]; then uv run pytest tests/integration -ra -x --durations=5; else echo "No integration tests yet"; fi

.PHONY: test-acceptance
test-acceptance: ## Run acceptance tests
	uv run pytest tests/acceptance -ra -x --durations=5

.PHONY: test
test: test-unit test-integration test-acceptance ## Run all the tests

.PHONY: watch
watch: ## Run all the tests in watch mode
	uv run ptw --runner "pytest tests -ra -x --durations=5"

.PHONY: coverage
coverage: ## Generate the coverage report
	uv run coverage run --branch -m pytest tests
	uv run coverage html
	@open "${PWD}/htmlcov/index.html"

.PHONY: pre-commit
pre-commit: checks test-unit

.PHONY: pre-push
pre-push: test-integration test-acceptance
