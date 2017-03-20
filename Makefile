init:
	pip install -r requirements.txt

test:
	py.test tests

run:
	python -i run.py -c default_config.yml

.PHONY: init test run
