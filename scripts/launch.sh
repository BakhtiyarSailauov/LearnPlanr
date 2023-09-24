#!/bin/sh

# Установка переменной окружения DJANGO_SETTINGS_MODULE
export DJANGO_SETTINGS_MODULE=bclproject.settings

# Сборка статических файлов Django
python manage.py collectstatic --noinput

# Применение миграций
echo 'Applying migrations...'
python manage.py migrate

# Запуск Gunicorn
gunicorn bclproject.wsgi:application --bind 0.0.0.0:$PORT
