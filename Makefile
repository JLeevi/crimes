.PHONY: start stop copy-dependencies ssh-container

start:
	docker compose up

stop:
	docker compose down

copy-dependencies:
	rm -rf local_dependencies
	docker cp crimes-airflow-webserver-1:/home/airflow/.local/lib/python3.8/site-packages ./local_dependencies

ssh-container:
	docker exec -it crimes-airflow-webserver-1 /bin/bash
