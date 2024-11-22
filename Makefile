.PHONY: start stop ssh-container

start:
	docker compose up

stop:
	docker compose down

ssh-container:
	docker exec -it crimes-airflow-webserver-1 /bin/bash
