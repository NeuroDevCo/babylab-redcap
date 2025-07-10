venv:
	python -m venv .venv

serve:
	python -m flask --app babylab.app run

debug:
	uv run flask --app babylab.app run --debug

test:
	uv run pytest -v -p no:cacheprovider --exitfirst --benchmark-time-unit="s" --benchmark-autosave

cov:
	uv run pytest -p no:cacheprovider --cov-report html --cov=babylab tests/

publish:
	hatch build
	hatch publish

lint:
	uv run pylint $(git ls-files '*.py')

docker-build:
	docker build --tag babylab-redcap .

docker-run:
	docker run -d -p 5000:5000 babylab-redcap

babel-extract:
	pybabel extract -F babel.cfg -o messages.pot .

babel-es:
	pybabel init -i messages.pot -d translations -l es

babel-compile:
	pybabel compile -d babylab/translations