# Perfume shop


Perfume shop is an online store created on Django + PostgreSQL and launched in conteiners using Docker



![image alt](https://github.com/ArtemRuban18/rubanarse-shop/blob/7f2149a32be1a58f20bc6e003f6fb22f5ccc3a67/shop_index_page.png)

## Tech Stack

- Backend: Django
- Database: PostgreSQL
- Caching & Message broker: Redis
- Task Queue: Celery
- Conteinerization: Docker, Docker-Compose
- Frontend: Django Templates & Bootstrap

## Features

- Product catalog
- Product filtering by name, category, type of flavor and price
- Product pagination
- Cart and order placement
- User authentication and registration 
- Ability to change a password
- Asynchronous task processing with Celery
- Redis as a caching backend for better perfomance
- Redis as message broker for Celery
- Logging

## Getting started

Follow these steps to set up and run project locally with Docker

## Prerequisites

Ensure that you have the following installed on your system

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

## Installation

Clone the repository:
   > git clone https://github.com/ArtemRuban18/rubanarse-shop

Create a .env file and configure environment variables

> cd rubanarse-shop
Build and run the containers:
   > docker-compose up --build

Create new database migrations:
   > docker-compose run django python manage.py makemigrations

Run database migrations:
   > docker-compose run django python manage.py migrate

Now you can run the server:
   > docker-compose run django python manage.py runserver

Create superuser:
   > docker-compose run django python manage.py createsuperuser

## Asynchronous Task

This project uses Celery for background tasks processing, powered by Redis as message broker
To start Celery, run
   > celery -A shop worker --loglevel=info

Check Redis connection:
   > docker-compose exec redis redis-cli
