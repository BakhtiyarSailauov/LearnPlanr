export DJANGO_SETTINGS_MODULE=bclproject.settings
python .\learn_planr\manage.py collectstatic --noinput
echo 'Applying migrations...'
python manage.py migrate

gunicorn bclproject.wsgi:application --bind 0.0.0.0:$PORT