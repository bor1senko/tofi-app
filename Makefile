backend-bash:
	@docker exec -ti $(shell docker-compose ps -q backend) bash

scoring-bash:
	@docker exec -ti $(shell docker-compose ps -q scoring) bash

backend-migrate:
	@docker exec -ti $(shell docker-compose ps -q backend) ./manage.py migrate

backend-runserver:
	@docker exec -ti $(shell docker-compose ps -q backend) ./manage.py runserver 0.0.0.0:8000

frontend-bash:
	@docker exec -ti $(shell docker-compose ps -q frontend) bash

frontend-reload:
	@docker exec -ti $(shell docker-compose ps -q frontend) nginx -s reload

db-shell:
	@docker exec -ti $(shell docker-compose ps -q db) psql -U jupiter

docker-restart:
	@docker-compose stop
	@docker-compose up

docker-recreate:
	@docker-compose stop ${service}
	@docker-compose rm -f ${service}
	@docker-compose up ${service}
