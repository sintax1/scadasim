init:
	pip install -r requirements.txt

test:
	py.test tests

run:
	python -i run.py -c default_config.yml

debug:
	python -i run.py -c default_config.yml -v 2

.PHONY: init test run debug
