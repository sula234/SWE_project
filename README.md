# SWE_project
## Starting the server
### Set up the Python environment and install dependencies
**Linux**
```
$ python -m venv venv
$ source venv/bin/activate
$ pip install django Pillow djangorestframework
```
**Windows**
```
$ python -m venv venv
$ .\venv\Scripts\activate 
$ pip install django Pillow djangorestframework
```
### Initialize Database
You need to run the following commands after first installing or after changing the models.py file
```
$ python manage.py makemigrations
$ python manage.py migrate
```
### Create superuser
Initially, there are no users in the database, to create a new superuser run
```
$ python manage.py createsuperuser
```
Other user types are created from the admin's home page
### Run the server
```
$ python manage.py runserver
```
