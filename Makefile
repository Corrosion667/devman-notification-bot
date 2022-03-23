install:
	poetry install

full-install:
	pip3 install --user poetry
	poetry install

run:
	poetry run bot

lint:
	poetry run flake8 bot