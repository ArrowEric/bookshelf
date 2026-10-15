.PHONY: test test-fast lint typecheck

test:
	pytest tests/

test-fast:
	pytest tests/unit/ -m "not slow"

lint:
	ruff check src/ && ruff format --check src/

typecheck:
	mypy src/
