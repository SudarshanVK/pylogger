# Makefile for Python project

# Python interpreter to use
PYTHON := python3

# Ruff configuration
RUFF_FLAGS := --fix

# Pytest configuration
PYTEST_FLAGS := -v

# Source and test directories
SRC_DIR := src
TEST_DIR := src/tests

# Default target
.PHONY: all
all: lint test

# Run Ruff for linting
.PHONY: lint
lint:
	@echo "Running Ruff..."
	poetry run ruff check . $(RUFF_FLAGS)

# Run pytest for testing
.PHONY: test
test:
	@echo "Running tests..."
	$(PYTHON) -m pytest $(TEST_DIR) $(PYTEST_FLAGS)

# Run both lint and test
.PHONY: check
check: lint test

# Clean up Python cache files
.PHONY: clean
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name "*.pytest_cache" -delete

# Help target
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  all    : Run both lint and test (default)"
	@echo "  lint   : Run Ruff for linting"
	@echo "  test   : Run pytest for testing"
	@echo "  check  : Run both lint and test"
	@echo "  clean  : Clean up Python cache files"
	@echo "  help   : Show this help message"
