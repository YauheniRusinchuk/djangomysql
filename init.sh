#!/bin/bash

# Create Django project
django-admin startproject core .

# Create a new app
python manage.py startapp main

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser --noinput 