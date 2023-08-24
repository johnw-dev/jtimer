clean:
	rm -rf dist
	find . -name __pycache__ | xargs rm -rf
	rm -rf assets

install:
	poetry install

run:
	poetry run python3 jtimer/main.py -l DEBUG

lint:
	poetry run black .

lint_check:
	poetry run black --check .
	poetry run bandit -c bandit.yml -r jtimer

test:
	poetry run pytest tests