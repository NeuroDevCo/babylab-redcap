test:
	uvx ruff format
	uvx ruff check --fix .
	uvx ty check
	uvx pytest -v --exitfirst
