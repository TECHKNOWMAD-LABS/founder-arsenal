.PHONY: test lint format security clean install help

# Default target
help:
	@echo "Founder Arsenal — Development Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  make install    Install dev dependencies"
	@echo "  make test       Run all tests with coverage"
	@echo "  make lint       Run ruff linter"
	@echo "  make format     Run ruff formatter"
	@echo "  make security   Run security scan (grep for secrets)"
	@echo "  make clean      Remove build artifacts"
	@echo "  make examples   Run all example scripts"

install:
	pip3 install pytest pytest-cov hypothesis ruff

test:
	python3 -m pytest -v --tb=short --cov=src --cov-report=term-missing

lint:
	python3 -m ruff check src/ tests/ --ignore E501 || true

format:
	python3 -m ruff format src/ tests/ || true

security:
	@echo "Scanning for secrets..."
	@grep -rn "password\s*=\s*['\"].\+['\"]" src/ tests/ 2>/dev/null || echo "  No hardcoded passwords"
	@grep -rn "api_key\s*=\s*['\"].\+['\"]" src/ tests/ 2>/dev/null || echo "  No hardcoded API keys"
	@grep -rn "secret\s*=\s*['\"].\+['\"]" src/ tests/ 2>/dev/null || echo "  No hardcoded secrets"
	@echo "Security scan complete."

examples:
	python3 examples/01_dispatch_founder_query.py
	python3 examples/02_crisis_assessment.py
	python3 examples/03_founder_dashboard.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	find . -name "*.pyo" -delete 2>/dev/null || true
	rm -rf .pytest_cache/ .coverage htmlcov/ dist/ build/ *.egg-info/ 2>/dev/null || true
	@echo "Clean complete."
