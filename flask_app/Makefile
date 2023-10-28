flask_app:
	poetry run flask --app app.main run
test:
	poetry run pytest .\tests\tests_app.py
	poetry run coverage run -m pytest .\tests\tests_app.py
	poetry run coverage html
	poetry run black ./
	poetry run ruff check --fix .
#	poetry run mypy ./
#	poetry run pylint ./src
build:
	docker build -t flask_app .
