# Используйте базовый образ Python 3.10
FROM python:3.10

# Установите переменную окружения для удобства разработки (можно удалить в production)
ENV DEBUG=True

# Установите рабочую директорию в контейнере в корневую папку проекта
WORKDIR /app

# Копируйте файлы pyproject.toml и poetry.lock из подпапки learn_planr
COPY pyproject.toml poetry.lock /app/

# Установите зависимости с использованием poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Копируйте остальные файлы проекта из директории learn_planr в контейнер
COPY learn_planr/ /app/

# Откройте порт, который будет использоваться Django (по умолчанию 8000)
EXPOSE 8000

# Запустите Django-приложение
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
