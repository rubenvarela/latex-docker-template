# =============================================================================
# LaTeX Template Repository - Makefile
# =============================================================================
# Build automation for LaTeX documents using Docker containers.
# All builds run inside Docker for reproducibility - no local LaTeX required.
#
# Run 'make help' to see all available targets.
# =============================================================================

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
SHELL := /bin/bash
.DEFAULT_GOAL := help

# Docker configuration
DOCKER_IMAGE := texlive/texlive:latest-full
DOCKER_RUN := docker run --rm -v "$(PWD)":/workspace -w /workspace

# Directories
SRC_DIR := src
BUILD_DIR := build
SCRIPTS_DIR := scripts
TESTS_DIR := tests
ASSETS_DIR := assets

# Main document
MAIN_TEX := $(SRC_DIR)/main.tex
TEST_TEX := $(TESTS_DIR)/test_document.tex

# Colors for terminal output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

# -----------------------------------------------------------------------------
# Phony Targets
# -----------------------------------------------------------------------------
.PHONY: help setup build test clean \
        watch build-draft build-test lint validate \
        build-local ci act act-test info check-deps open docker-pull

# =============================================================================
# Primary Targets (Required)
# =============================================================================

## setup: Check Docker and pull the LaTeX image
setup:
	@echo -e "$(BLUE)Setting up environment...$(NC)"
	@./$(SCRIPTS_DIR)/setup.py
	@echo -e "$(GREEN)✓ Setup complete!$(NC)"

## build: Compile the main LaTeX document (using Docker)
build:
	@echo -e "$(BLUE)Building LaTeX document in Docker...$(NC)"
	@./$(SCRIPTS_DIR)/build.py --src $(MAIN_TEX) --output $(BUILD_DIR)
	@echo -e "$(GREEN)✓ Build complete: $(BUILD_DIR)/main.pdf$(NC)"

## test: Run tests in Docker to verify setup works
test:
	@echo -e "$(BLUE)Running tests in Docker...$(NC)"
	@./$(SCRIPTS_DIR)/test.py
	@echo -e "$(GREEN)✓ Tests complete!$(NC)"

## clean: Remove all build artifacts
clean:
	@echo -e "$(YELLOW)Cleaning build artifacts...$(NC)"
	@./$(SCRIPTS_DIR)/clean.py
	@echo -e "$(GREEN)✓ Clean complete!$(NC)"

# =============================================================================
# Additional Build Targets
# =============================================================================

## build-draft: Quick draft build (single pass, no bibliography)
build-draft:
	@echo -e "$(BLUE)Building draft in Docker...$(NC)"
	@./$(SCRIPTS_DIR)/build.py --src $(MAIN_TEX) --output $(BUILD_DIR) --draft
	@echo -e "$(GREEN)✓ Draft build complete!$(NC)"

## build-test: Build the test document to verify all packages
build-test:
	@echo -e "$(BLUE)Building test document in Docker...$(NC)"
	@./$(SCRIPTS_DIR)/build.py --src $(TEST_TEX) --output $(BUILD_DIR)
	@echo -e "$(GREEN)✓ Test document built!$(NC)"

## watch: Watch for changes and auto-rebuild (using Docker)
watch:
	@echo -e "$(BLUE)Starting watch mode (Ctrl+C to stop)...$(NC)"
	@./$(SCRIPTS_DIR)/watch.py --src $(SRC_DIR) --output $(BUILD_DIR)

# =============================================================================
# Quality & Validation
# =============================================================================

## lint: Run LaTeX linter (chktex) in Docker
lint:
	@echo -e "$(BLUE)Running LaTeX linter in Docker...$(NC)"
	@./$(SCRIPTS_DIR)/lint.py --src $(SRC_DIR)
	@echo -e "$(GREEN)✓ Lint complete!$(NC)"

## validate: Validate LaTeX syntax without full compilation
validate:
	@echo -e "$(BLUE)Validating LaTeX syntax...$(NC)"
	@./$(SCRIPTS_DIR)/build.py --src $(MAIN_TEX) --output $(BUILD_DIR) --validate-only
	@echo -e "$(GREEN)✓ Validation complete!$(NC)"

# =============================================================================
# Local Build Targets (requires local LaTeX installation)
# =============================================================================

## build-local: Build using local LaTeX installation (not Docker)
build-local:
	@echo -e "$(BLUE)Building with local LaTeX...$(NC)"
	@mkdir -p $(BUILD_DIR)
	@cd $(SRC_DIR) && latexmk -pdf -shell-escape -interaction=nonstopmode \
		-output-directory=../$(BUILD_DIR) main.tex
	@echo -e "$(GREEN)✓ Local build complete!$(NC)"

# =============================================================================
# Docker Targets
# =============================================================================

## docker-pull: Pull the LaTeX Docker image
docker-pull:
	@echo -e "$(BLUE)Pulling Docker image...$(NC)"
	@docker pull $(DOCKER_IMAGE)
	@echo -e "$(GREEN)✓ Image pulled!$(NC)"

## docker-shell: Open a shell in the Docker container
docker-shell:
	@echo -e "$(BLUE)Opening Docker shell...$(NC)"
	@$(DOCKER_RUN) -it $(DOCKER_IMAGE) /bin/bash

# =============================================================================
# CI/CD Targets
# =============================================================================

## ci: Run full CI pipeline locally
ci: setup lint build-test build
	@echo -e "$(GREEN)✓ CI pipeline complete!$(NC)"

## act: Run GitHub Actions locally using act (requires act installed)
act:
	@echo -e "$(BLUE)Running GitHub Actions with act...$(NC)"
	@command -v act >/dev/null 2>&1 || { echo -e "$(RED)✗ act not installed. Install: brew install act$(NC)"; exit 1; }
	@act push
	@echo -e "$(GREEN)✓ GitHub Actions complete!$(NC)"

## act-test: Test GitHub Actions build job with act (faster, build only)
act-test:
	@echo -e "$(BLUE)Testing GitHub Actions build job with act...$(NC)"
	@command -v act >/dev/null 2>&1 || { echo -e "$(RED)✗ act not installed. Install: brew install act$(NC)"; exit 1; }
	@act push --job build
	@echo -e "$(GREEN)✓ GitHub Actions build test complete!$(NC)"

# =============================================================================
# Utility Targets
# =============================================================================

## check-deps: Check if Docker is installed and running
check-deps:
	@echo -e "$(BLUE)Checking dependencies...$(NC)"
	@command -v docker >/dev/null 2>&1 || { echo -e "$(RED)✗ Docker not found$(NC)"; exit 1; }
	@docker info >/dev/null 2>&1 || { echo -e "$(RED)✗ Docker not running$(NC)"; exit 1; }
	@echo -e "$(GREEN)✓ Docker is available!$(NC)"

## info: Display project information
info:
	@echo -e "$(BLUE)Project Information$(NC)"
	@echo "===================="
	@echo "Main document: $(MAIN_TEX)"
	@echo "Test document: $(TEST_TEX)"
	@echo "Output directory: $(BUILD_DIR)"
	@echo "Docker image: $(DOCKER_IMAGE)"
	@echo ""
	@echo "Docker version:"
	@docker --version

## open: Open the compiled PDF (macOS)
open:
	@if [ -f "$(BUILD_DIR)/main.pdf" ]; then \
		open "$(BUILD_DIR)/main.pdf"; \
	else \
		echo -e "$(RED)✗ PDF not found. Run 'make build' first.$(NC)"; \
	fi

## help: Display this help message
help:
	@echo -e "$(BLUE)LaTeX Template Repository$(NC)"
	@echo "=========================="
	@echo ""
	@echo "All builds run inside Docker - no local LaTeX installation required."
	@echo "Just install Docker and run 'make setup' to get started."
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Primary Targets:"
	@echo "  setup       Check Docker and pull the LaTeX image"
	@echo "  build       Compile the main document (Docker)"
	@echo "  test        Run tests to verify setup (Docker)"
	@echo "  clean       Remove all build artifacts"
	@echo ""
	@echo "Build Targets:"
	@echo "  build-draft Quick draft build (single pass)"
	@echo "  build-test  Build the test document"
	@echo "  watch       Watch for changes and auto-rebuild"
	@echo ""
	@echo "Quality:"
	@echo "  lint        Run LaTeX linter (chktex)"
	@echo "  validate    Validate LaTeX syntax"
	@echo ""
	@echo "Docker:"
	@echo "  docker-pull   Pull the LaTeX Docker image"
	@echo "  docker-shell  Open a shell in the container"
	@echo ""
	@echo "Local (requires LaTeX installed):"
	@echo "  build-local Build without Docker"
	@echo ""
	@echo "CI/CD:"
	@echo "  ci          Run full CI pipeline locally"
	@echo "  act         Run GitHub Actions with act (requires act)"
	@echo "  act-test    Test GitHub Actions build job only (faster)"
	@echo ""
	@echo "Other:"
	@echo "  check-deps  Check Docker availability"
	@echo "  info        Display project information"
	@echo "  open        Open the compiled PDF"
	@echo "  help        Display this help message"

# =============================================================================
# End of Makefile
# =============================================================================
