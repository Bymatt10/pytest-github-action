## ROCC API

API REST para registro de variables climáticas como pricipitacción, temperatura, etc.

### Requirements

- Python 3+
- Django 5
- Django Rest Framework
- Simple JWT
- Sqlite/Postgresql
- Swagger
- pytest

### Features

- Auth JWT
- CRUD locations
- CRUD organizations
- CRUD stations, equipments, rainfall
- Rainfall history

### Run app

```
pip install -r requirements.txt

Rename .example to .env

python manage.py migrate
python manage.py createaccount
python manage.py runserver

```

### Swagger API

- http://127.0.0.1:8000/swagger/


### Run unit tests

```
pytest

```

### Run translations
```
python manage.py makemessages -l es
python manage.py makemessages -l en
python manage.py compilemessages

```