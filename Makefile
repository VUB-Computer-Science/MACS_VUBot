build:
	docker build -t macs_vubot .

run:
	docker run -d --name macs_vubot macs_vubot:latest
