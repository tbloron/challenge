# Shop project
[![Python Version](https://img.shields.io/badge/python-3.9-brightgreen.svg)](https://python.org)
[![Django Version](https://img.shields.io/badge/django-3.2-brightgreen.svg)](https://www.djangoproject.com)

Web application built by django framework.

## Overview
The **shop** project contains three applications:
  * **users**, for the management of users (both staff and customer)
  * **products**, for the management of products
  * **sells**, for the management of orders

## Header for administrators
The header of the Shop for administrators contains:
  * **Products**, to manage the available products (add, update, delete),
  * **Orders**, to view the validated orders of all the customers,
  * **Customers**, to register new users as administrators or customers (Django Administration view of users)
  * **Log out**, to log out from the App.

## Header for customers
The header of the Shop for customers contains:
  * **Products**, to see all the available products and add them to their basket,
  * **Orders**, to view the validated orders (history on previous orders),
  * **Basket**, to see the content of the basket and update it (remove products, increment/decrement quantity of a product)
  * **Log out**, to log out from the App.

	
## Running project
Install require packages

	pip install -r requirements.txt

Migrate project

	python3 manage.py migrate

Create a superuser

	python3 manage.py createsuperuser

Run your server on your localhost

	python3 manage.py runserver

## Running tests

	python3 manage.py test
