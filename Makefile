install:
	# install commands
	pip install -r requirements.txt
uninstall:
	pip freeze --local | grep -v "^-e" | cut -d = -f 1 | xargs -n 1 pip uninstall -y
format:
	# format code
	black *.py ./src
lint:
	# flake8 or pylint
	pylint --disable=R,C *.py ./src/**/*.py main_app.py
test:
	#test
	python -m pytest -vv --cov=mylib test_logic.py
deploy:
	#deploy
all: install lint test deploy

# commands
compose-up:
	docker compose -f docker-compose.yml up --build -d
compose-down:
	docker compose -f docker-compose.yml down
compose-logs:
	docker compose -f docker-compose.yml logs -f
compose-restart:
	docker compose -f docker-compose.yml down && docker compose -f docker-compose.yml up --build -d
compose-clean:
	docker compose -f docker-compose.yml down -v

help:
	@echo "Comandos disponibles:"
	@echo "  compose-up        - Builds and starts the services in detached mode."
	@echo "  compose-down      - Stops the services and removes the containers."
	@echo "  compose-logs      - Follows the logs of all services."
	@echo "  compose-restart   - Restarts the services by shutting them down and starting them again with a rebuild."
	@echo "  compose-clean     - Stops the services, removes containers, and deletes volumes ... useful for a fresh start"
