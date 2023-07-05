clean:
	rm -rf dist
	find . -name __pycache__ | xargs rm -rf
	rm -rf assets

run:
	poetry run python3 mptimer/main.py

lint:
	poetry run black .

lint_check:
	poetry run black --check .
	poetry run bandit -r function
	poetry run safety check

test:
	poetry run pytest tests