test:
	uv ruff format
	uv ruff check
	uv run pytest -v -p no:cacheprovider --exitfirst --benchmark-time-unit="s" --benchmark-autosave

cov:
	uv run pytest --cov=babylab
