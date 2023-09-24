# Этап установки зависимостей
FROM python:3.10 as requirements-stage

WORKDIR /tmp/learn_planr/
RUN pip install poetry==1.5.0
COPY pyproject.toml poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Этап выполнения приложения
FROM python:3.10 as app-stage

WORKDIR /code
COPY --from=requirements-stage /tmp/requirements.txt .
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

# Копируйте содержимое каталога learn_planr в контейнер
COPY learn_planr/ /code/

CMD ["sh", "scripts/launch.sh"]
