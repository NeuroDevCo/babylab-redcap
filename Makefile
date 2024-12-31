.PHONY: changelog, version-patch

changelog:
	powershell.exe -Command 'git log -1 --pretty=format:"- %s" | Out-File -Append -FilePath ./CHANGELOG.md -Encoding utf8'

venv:
	python -m venv .venv

serve:
	python -m flask --app babylab.app run

debug:
	python -m flask --app babylab.app run --debug

freeze:
	python -m pip freeze -l > requirements.txt 

install:
	python -m pip install -r requirements.txt

test:
	python -m pytest -v -p no:cacheprovider

cov:
	python -m pytest -p no:cacheprovider --cov-report html --cov=babylab tests/

version-patch:
	hatch version patch
	$version = hatch version
	$versionWithV = "v" + $version
	git add babylab/app/__about__.py
	git commit -m $versionWithV
	git push