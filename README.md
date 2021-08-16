# demo-python-django-api

Django codebase for Todo list

### Prerequisites

- Python 3.9
- pip3
- Django 3.2.6

Check requirements.txt to see all requirements  

## Installation

From terminal

```
#install dependencies
pip install -r requirements.txt

#copy file and set proper data inside
cp .env.example .env

#docker setup
docker-compose up --build #or install postgres manually

```

### Migrate Database:
```
python manage.py migrate users
python manage.py migrate to_do
python manage.py migrate
```


### Create Super User(Admin)
```
python manage.py createsuperuser
```

Write the data for admin account 

### Seeder - populate database with fake data
```
python manage.py seed ToDo --number=15
```

### Run Server 
```
python manage.py runserver
```

or
```    
python manage.py runserver Port_number(for example 7000)
```


### Run Tests
```
python manage.py test
```

## Documentation

There are two ways to use API documentation. 
They are generated automatically after running server.

```
Swagger:
127.0.0.1:8000/api/
ReDoc: 
127.0.0.1:8000
```