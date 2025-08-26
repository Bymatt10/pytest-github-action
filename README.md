## ROCC API

API REST para registro de variables climáticas como pricipitacción, temperatura, etc.

### Paquetes

- Python 3+
- Django 5
- Django Rest Framework
- Simple JWT
- Sqlite/Postgresql
- Swagger

### Funcionalidades

- Autenticación JWT
- CRUD ubicaciones
- CRUD organizaciones
- CRUD estaciones, equipos, precipitacion
- Registro de normas historicas

### Ejecutar app

```
pip install -r requirements.txt

Renombrar archivo .example a .env y configurar variables de entorno

python manage.py migrate
python manage.py createaccount
python manage.py runserver

```

### Swagger API

- http://127.0.0.1:8000/swagger/