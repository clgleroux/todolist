venv:
	python3 -m venv venv

yarn:
	cd ./todolist/tasks/static/tasks/vendor && yarn install

update:
	./venv/bin/pip install -U -r requierements.txt

install: venv yarn update migrate

test:
	cd ./todolist && ../venv/bin/python ./manage.py test

migrate:
	cd ./todolist && ../venv/bin/python ./manage.py migrate

run:
	cd ./todolist && ../venv/bin/python ./manage.py runserver
