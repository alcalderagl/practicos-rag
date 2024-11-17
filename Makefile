install:
	# install commands
	pip install --upgrade pip &&\
	pip install -r requirements.txt
uninstall:
	pip freeze --local | grep -v "^-e" | cut -d = -f 1 | xargs -n 1 pip uninstall -y
format:
	# format code
	black *.py ./src/**/*.py
lint:
	# flake8 or pylint
	pylint --disable=R,C *.py ./src/**/*.py main_app.py
test:
	#test
	python -m pytest -vv --cov=mylib test_logic.py
deploy:
	#deploy
all: install lint test deploy
