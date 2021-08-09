#demo-python-django-api

## Installation

### env
Create file .env and write your DB configuration 

For Postgresql: 

    DATABASE_DIALECT=postgresql_psycopg2

For MySQL:

    DATABASE_DIALECT=mysql


###Migrate Database:

    python manage.py migrate users
    python manage.py migrate to_do
    python manage.py migrate

###Create Super User(Admin)
    python manage.py createsuperuser

Write the data for admin account 

###Seeder - populate database with fake data
    python manage.py seed ToDo --number=15

###Run Server 
    python manage.py runserver

or
    
    python manage.py runserver Port_number(for example 7000)


###Run Tests
    python manage.py test
