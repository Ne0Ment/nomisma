.PHONY: up
up:
	docker-compose -p obligiru up --build -d
	docker image prune -af
	
.PHONY: down
down:
	docker-compose -p obligiru down
