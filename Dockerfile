# Этап установки зависимостей
FROM python:3.10 as requirements-stage

# Устанавливаем Poetry
RUN pip install poetry==1.1.5

# Создаем рабочую директорию
WORKDIR /app

# Копируем файлы pyproject.toml и poetry.lock
COPY pyproject.toml poetry.lock /app/

# Экспортируем зависимости в формате requirements.txt без хешей
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Этап выполнения приложения
FROM python:3.10 as app-stage

# Создаем рабочую директорию
WORKDIR /code

# Копируем requirements.txt из предыдущего этапа
COPY --from=requirements-stage /app/requirements.txt /code/

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Копируем все остальные файлы из текущего контекста (проект)
COPY . .

# Запускаем скрипт launch.sh
CMD ["sh", "scripts/launch.sh"]
