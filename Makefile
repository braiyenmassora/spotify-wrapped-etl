.PHONY: help setup extract transform pipeline dashboard clean lint format remove-token

help:
	@echo "============================================"
	@echo "Spotify Wrapped ETL - Makefile Commands"
	@echo "============================================"
	@echo "  make setup         - setup venv & install dependencies"
	@echo "  make extract       - extract data from spotify api"
	@echo "  make transform     - transform raw data"
	@echo "  make pipeline      - run full etl (extract + transform)"
	@echo "  make dashboard     - start streamlit dashboard"
	@echo "  make clean         - remove data & cache"
	@echo "  make remove-token  - remove spotify token cache"
	@echo "  make lint          - check code style (black, flake8)"
	@echo "  make format        - auto-format code with black"
	@echo ""

setup:
	python3.11 -m venv .venv
	.venv/bin/pip install --upgrade pip pip-tools
	.venv/bin/pip-compile requirements.in
	.venv/bin/pip install -r requirements.txt

extract:
	.venv/bin/python -m src.jobs.extract

transform:
	.venv/bin/python -m src.jobs.transform

pipeline: extract transform

dashboard:
	.venv/bin/streamlit run dashboard/app.py

remove-token:
	rm -f .spotify_cache

clean:
	rm -rf data/raw/ data/processed/
	rm -f .spotify_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

lint:
	.venv/bin/black --check src/
	.venv/bin/flake8 src/ --max-line-length=100

format:
	.venv/bin/black src/