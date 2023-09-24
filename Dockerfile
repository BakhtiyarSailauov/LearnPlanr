# Используйте базовый образ Python 3.8
FROM python:3.11

# Установите переменную окружения для удобства разработки (это можно удалить в production)
ENV DEBUG=True

# Установите рабочую директорию в контейнере в корневую папку проекта
WORKDIR /app

# Копируйте файлы pyproject.toml и poetry.lock в контейнер
COPY pyproject.toml poetry.lock /app/

# Установите зависимости с использованием poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Копируйте остальные файлы проекта в контейнер
COPY . /app/

# Откройте порт, который будет использоваться Django (по умолчанию 8000)
EXPOSE 8000

# Запустите Django-приложение
CMD ["poetry", "run", "python", "./learn_planr/manage.py", "runserver", "0.0.0.0:8000"]
