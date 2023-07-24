build: stop
	docker build --target crud -t crud .

start:
	docker compose up

stop:
	docker compose down
