build:
	docker build -t macs_vubot .

run:
	docker stop macs_vubot || true && docker rm macs_vubot || true
	docker run -d --name macs_vubot macs_vubot:latest

check:
	poetry run black --check --diff .
	poetry run pflake8 .
	poetry run isort --check --diff .
