release: python manage.py migrate --run-syncdb
web: gunicorn quasar_fire.wsgi --log-file -
