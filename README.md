# Big Corp Shop Project

## Описание
Big Corp Shop Project - это Django ecommerce проект с API и различными функциями.


## Установка
Чтобы запустить проект, выполните следующие шаги:
1. Соберите проект локально с помощью Docker Compose: docker-compose build
2. Запустите проект: docker-compose up -d

## Использование
1. После запуска проекта создайте суперпользователя с помощью следующей команды: $ sudo docker exec -it bigcorp-backend python manage.py createsuperuser
2. Зайдите в интерфейс администратора в браузере и вручную создайте хотя бы одну категорию для товаров.
3. Создайте поддельные продукты с помощью следующей команды: $ sudo docker exec -it bigcorp-backend python manage.py fakeproducts

## Используемые технологии
Этот проект построен с использованием следующих технологий:
- Python
- JavaScript
- Ajax
- CSS
- HTML
- Postgres
- Celery Beat
- Celery Result
- Celery
- Брокер Redis
- Django Htmx
- Nginx
- Gunicorn
- API
- Swagger и Redoc Docs
- Stripe
- Yookassa
- Django Rest Framework
- Docker
- Docker Compose
- GitHub
- Git
