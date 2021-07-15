#demo-python-django-api

## Instalation

### env
Create file .env and write your DB configuration 

For Postgresql: 

    DATABASE_DIALECT=postgresql_psycopg2

For MySQL:

    DATABASE_DIALECT=mysql


###Migrate Database:
    python manage.py migrate

###Create Super User(Admin)
    python manage.py createsuperuser

Write the data for admin account 

###Seeder - populate database with fake data
    python manage.py seed ToDo --number=15

###Run Server 
    python manage.py runserver

