# Используйте базовый образ Python 3.10
FROM python:3.10

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

RUN pip install gunicorn

# Запустите Django-приложение
CMD ["sh", "scripts/launch.sh"]
