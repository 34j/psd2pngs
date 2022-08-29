.PHONY: deploy
deploy: build
	twine upload dist/*.tar.gz

.PHONY: test-deploy
test-deploy: build
	twine upload -r testpypi dist/*.tar.gz

.PHONY: build
build:
	python setup.py sdist

.PHONY: docs
docs:
	cd docs
	sphinx-apidoc --force --output-dir source/ ../psd2pngs/ --module-first --no-toc
	./make.bat html

.PHONY: exe
exe:
	pyinstaller psd2pngs/__main__.py --onefile -n psd2pngs

.PHONY: license
license:
	pip install -U pip-licenses
	pip-licenses --order license --format markdown --output-file PackageLicenses.md -i pyinstaller pyinstaller-hooks-contrib

.PHONY: venv
venv:
	py -m venv venv
	"./venv/Scripts/Activate.bat"
	pip install -r requirements_dev.txt