Запуск проекта
Установить зависимости:

poetry install
Войти в окружение poetry:

poetry shell
Открыть папку с manage.py

cd .\learn_planr\ 
Запустить Django-приложение.

python .\manage.py runserver
После этого сервер запуститься на порту 8000. Чтобы проверить подключение сделайте запрос на localhost:8000.

curl http://127.0.0.1:8000/
