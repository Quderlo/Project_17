migrate:
	venv/Scripts/python.exe src/manage.py makemigrations
	venv/Scripts/python.exe src/manage.py migrate
