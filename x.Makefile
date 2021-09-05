all: clean install
install:
	python3 setup.py install -f
clean:
	find . -name '#*#' | xargs rm -fr
	find . -name '*~' | xargs rm -fr
	find . -name '__pycache__' | xargs rm -fr
	rm -fr dist *.egg-info build ?
	tree .
