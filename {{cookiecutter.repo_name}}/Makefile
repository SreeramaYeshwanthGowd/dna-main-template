PROJECT_TYPE := {{ cookiecutter.__project_type}}
PYTHON_DIR := {{ cookiecutter.__python_package_name }}
SCALA_DIR := {{ cookiecutter.__scala_package_name }}

{% if cookiecutter.__databricks_enabled == "yes" %}
DATABRICKS_PROFILE ?= {{ cookiecutter.__databricks_profile }}
DATABRICKS_TEMPLATE ?= default-python
{% endif %}

SHELL := /bin/bash
.SHELLFLAGS := -eu -o pipefail -c

{% if cookiecutter.__databricks_enabled == "yes" %}
.PHONY: setup build test validate deploy databricks-init ci help
{% else %}
.PHONY: setup build test ci help
{% endif %}

# Setup

setup:
ifeq ($(PROJECT_TYPE),python)
	@echo "Setting up Python environment..."
	cd $(PYTHON_DIR) && python3 -m venv .venv
endif

ifeq ($(PROJECT_TYPE),scala)
	@echo "Resolving Scala dependencies..."
	cd $(SCALA_DIR) && sbt update
endif

ifeq ($(PROJECT_TYPE),hybrid)
	@echo "Setting up Hybrid project..."
	cd $(PYTHON_DIR) && python3 -m venv .venv
	cd $(SCALA_DIR) && sbt update
endif


# Build


build:
ifeq ($(PROJECT_TYPE),python)
	@echo "Building Python project..."
	cd $(PYTHON_DIR) && python3 -m compileall src
endif

ifeq ($(PROJECT_TYPE),scala)
	@echo "Building Scala project..."
	cd $(SCALA_DIR) && sbt compile
endif

ifeq ($(PROJECT_TYPE),hybrid)
	@echo "Building Hybrid project..."
	cd $(PYTHON_DIR) && python3 -m compileall src
	cd $(SCALA_DIR) && sbt compile
endif


# Test


test:
ifeq ($(PROJECT_TYPE),python)
	@echo "Running Python tests..."
	cd $(PYTHON_DIR) && pytest
endif

ifeq ($(PROJECT_TYPE),scala)
	@echo "Running Scala tests..."
	cd $(SCALA_DIR) && sbt test
endif

ifeq ($(PROJECT_TYPE),hybrid)
	@echo "Running Hybrid tests..."
	cd $(PYTHON_DIR) && pytest
	cd $(SCALA_DIR) && sbt test
endif


{% if cookiecutter.__databricks_enabled == "yes" %}
# Databricks Bundle Init


databricks-init:
	@echo "Initializing Databricks bundle..."

	@if [ ! -f databricks.yml ]; then \
		databricks bundle init $(DATABRICKS_TEMPLATE) \
			--profile $(DATABRICKS_PROFILE) \
			--output-dir . \
			--force; \
	else \
		echo "databricks.yml already exists. Skipping init."; \
	fi


# Databricks Validate


validate:
	@echo "Validating Databricks bundle..."

	@if [ ! -f databricks.yml ]; then \
		echo "ERROR: databricks.yml not found."; \
		echo "Run: make databricks-init"; \
		exit 1; \
	fi

	databricks bundle validate -p $(DATABRICKS_PROFILE)

deploy:
	@echo "Deploying Databricks bundle..."
	databricks bundle deploy -p $(DATABRICKS_PROFILE)
{% endif %}

# Full CI Flow


{% if cookiecutter.__databricks_enabled == "yes" %}
ci: build test validate
{% else %}
ci: build test
{% endif %}


# Help


help:
	@echo ""
	@echo "Available commands:"
	@echo ""
	@echo "  make setup"
	@echo "  make build"
	@echo "  make test"
{% if cookiecutter.__databricks_enabled == "yes" %}
	@echo "  make databricks-init"
	@echo "  make validate"
	@echo "  make deploy"
{% endif %}
	@echo "  make ci"
	@echo ""