export DJANGO_SETTINGS_MODULE=learn_planr.settings
python learn_planr/manage.py collectstatic --noinput
echo 'Applying migrations...'
python learn_planr/manage.py migrate

gunicorn learn_planr.learn_planr.wsgi:application --bind 0.0.0.0:$PORT
