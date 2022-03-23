install:
	poetry install --no-root

full-install:
	pip3 install --user poetry
	poetry install --no-root

run:
	poetry run bot

lint:
	poetry run flake8 bot