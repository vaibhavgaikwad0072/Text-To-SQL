.PHONY: help install setup test run-web run-cli run-interactive clean logs

# Default target
help:
	@echo "Text-to-SQL Pipeline - Available Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install        - Install dependencies"
	@echo "  make setup          - Complete setup (install + environment)"
	@echo ""
	@echo "Running:"
	@echo "  make run-web        - Start Streamlit web interface"
	@echo "  make run-cli        - Run single CLI query (QUERY='your question')"
	@echo "  make run-interactive - Run interactive CLI mode"
	@echo ""
	@echo "Testing & Maintenance:"
	@echo "  make test           - Run test suite"
	@echo "  make logs           - View application logs"
	@echo "  make clean          - Clean up generated files"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo ""

# Installation
install:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "✓ Dependencies installed"

setup: install
	@echo "Setting up environment..."
	python setup.py
	@echo "✓ Setup complete"

# Running
run-web:
	streamlit run app.py

run-cli:
	@if [ -z "$(QUERY)" ]; then \
		echo "Usage: make run-cli QUERY='your question'"; \
		exit 1; \
	fi
	python cli.py "$(QUERY)"

run-interactive:
	python cli.py --interactive

# Testing
test:
	@echo "Running test suite..."
	python test_pipeline.py

# Maintenance
logs:
	@if [ -f "logs/text_to_sql.log" ]; then \
		tail -f logs/text_to_sql.log; \
	else \
		echo "No logs found. Run some queries first."; \
	fi

clean:
	@echo "Cleaning up..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	@echo "✓ Cleanup complete"

# Docker commands
docker-build:
	docker build -t text-to-sql:latest .

docker-up:
	docker-compose up -d
	@echo "✓ Services started"
	@echo "  Web UI: http://localhost:8501"
	@echo "  MySQL: localhost:3306"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Development helpers
freeze:
	pip freeze > requirements-frozen.txt
	@echo "✓ Dependencies frozen to requirements-frozen.txt"

format:
	python -m black . --line-length 100
	@echo "✓ Code formatted"

lint:
	python -m pylint **/*.py
	@echo "✓ Linting complete"
