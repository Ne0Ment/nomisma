.PHONY: up
up:
	docker-compose -p obligiru up --build -d
	
.PHONY: down
down:
	docker-compose -p obligiru down
	
