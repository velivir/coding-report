install:
		poetry install --no-dev

dev_install:
		poetry install

lint:
		poetry run mypy coding_report
		poetry run flake8 coding_report

run:
		poetry run python coding_report/run.py
