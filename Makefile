venv:
	python3 -m venv venv

update:
	./venv/bin/pip install -U -r requierements.txt

install: venv update migrate

test:
	cd ./todolist && ../venv/bin/python ./manage.py test

migrate:
	cd ./todolist && ../venv/bin/python ./manage.py migrate

run:
	cd ./todolist && ../venv/bin/python ./manage.py runserver
