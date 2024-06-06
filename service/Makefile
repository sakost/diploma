FORMAT_DIRS=app migrations tests
LINTER_DIRS=app migrations tests
TOML_FILES=poetry.lock pyproject.toml
POETRY_EXEC=poetry
PYTHON_EXEC=$(POETRY_EXEC) run python

.PHONY: help
help:  ## Print this message
	@grep -E -h '\s##\s' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.PHONY: install
install:  ## Install dependencies
	poetry install

.PHONY: pretty
pretty: isort black  ## Make formatting of code

.PHONY: lint
lint: pylint mypy flake8 bandit  ## Check code by linters

.PHONY: black
black:
	$(PYTHON_EXEC) -m black -t py311 $(FORMAT_DIRS)

.PHONY: isort
isort:
	$(PYTHON_EXEC) -m isort $(FORMAT_DIRS)

.PHONY: mypy
mypy:
	$(POETRY_EXEC) run mypy --show-error-codes --python-version=3.11 $(LINTER_DIRS) || true

.PHONY: flake8
flake8:
	$(POETRY_EXEC) run flake8 --jobs 4 --statistics --show-source $(LINTER_DIRS) || true

.PHONY: pylint
pylint:
	$(POETRY_EXEC) run pylint --jobs 4 --rcfile=setup.cfg --extension-pkg-whitelist='pydantic' $(LINTER_DIRS) || true

.PHONY: bandit
bandit:
	$(POETRY_EXEC) run bandit -r $(LINTER_DIRS) || true

.PHONY: test
test:  ## Run unit-tests
	$(POETRY_EXEC) run pytest -m tests/ -vvv -Wignore
