migrate:
	venv/Scripts/python.exe src/manage.py makemigrations people recognition
	venv/Scripts/python.exe src/manage.py migrate
