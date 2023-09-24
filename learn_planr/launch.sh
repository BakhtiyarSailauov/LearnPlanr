export DJANGO_SETTINGS_MODULE=bilim_ai.settings
python manage.py collectstatic --noinput
echo 'Applying migrations...'
python manage.py migrate

gunicorn learn_planr.wsgi:application --bind 0.0.0.0:$PORT