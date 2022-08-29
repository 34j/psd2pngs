.PHONY: deploy
deploy: build
	twine upload dist/*.tar.gz

.PHONY: test-deploy
test-deploy: build
	twine upload -r testpypi dist/*.tar.gz

.PHONY: build
build:
	python setup.py sdist