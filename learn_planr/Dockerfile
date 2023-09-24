# Используйте базовый образ Python 3.10
FROM python:3.10

# Установите переменную окружения для удобства разработки (можно удалить в production)
ENV DEBUG=True

# Установите рабочую директорию в контейнере в корневую папку проекта
WORKDIR /app

# Копируйте файлы pyproject.toml и poetry.lock из подпапки learn_planr
COPY Learn_planr/learn_planr/pyproject.toml Learn_planr/learn_planr/poetry.lock /app/

# Установите зависимости с использованием poetry
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

# Копируйте остальные файлы и каталоги проекта в контейнер
COPY Learn_planr/learn_planr/ /app/learn_planr/

# Откройте порт, который будет использоваться Django (по умолчанию 8000)
EXPOSE 8000

# Запустите Django-приложение
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
