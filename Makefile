init:
	pip install -r requirements.txt

test:
	py.test tests

run:
	python -i run.py -c default_config.yml -d

debug:
	python -i run.py -c default_config.yml -d -v

.PHONY: init test run debug
