.DEFAULT_GOAL := help

.PHONY: help
help:  ## Show this help.
	@grep -E '^\S+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "%-30s %s\n", $$1, $$2}'

.PHONY: install
install: ## Install the app packages
	npm install

.PHONY: dev
dev: ## Run the app in development mode (proxies /api to localhost:8000)
	npm run dev

.PHONY: build
build: ## Type-check and build the production bundle
	npm run build

.PHONY: preview
preview: ## Preview the production bundle locally
	npm run preview

.PHONY: docker-build
docker-build: ## Build the docker image
	docker build -t pdd-creator-frontend .

.PHONY: check-lint
check-lint: ## Check the code style
	npm run lint

.PHONY: lint
lint: ## Fix lint issues
	npm run lint:fix

.PHONY: check-format
check-format: ## Check the code format
	npm run format:check

.PHONY: format
format: ## Format the code
	npm run format

.PHONY: check-typing
check-typing: ## Run the TypeScript compiler without emitting
	npm run typecheck

.PHONY: checks
checks: check-lint check-format check-typing ## Run all checks

.PHONY: test
test: ## Run the test suite
	npm test

.PHONY: watch
watch: ## Run the tests in watch mode
	npm run test:watch

.PHONY: pre-commit
pre-commit: checks test
