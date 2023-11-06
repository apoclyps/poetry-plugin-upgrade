.PHONY: help lint test

default: help

help: ## show this help
	@echo
	@fgrep -h " ## " $(MAKEFILE_LIST) | fgrep -v fgrep | sed -Ee 's/([a-z.]*):[^#]*##(.*)/\1##\2/' | column -t -s "##"
	@echo

env: ## Create a virtual environment
	poetry install --sync
	poetry shell

lint: env ## Lint and format the code
	black .
	ruff check .
	mypy --ignore-missing-imports -p src
	codespell .
	refurb .

test: env ## Run the unit tests and linters
	pytest -vv --cov=src --cov-report=term-missing --cov-fail-under=50 tests
