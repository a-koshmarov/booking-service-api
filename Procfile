release: python manage.py makemigrations
release: python manage.py migrate

web: waitress-serve --port=$PORT booking.wsgi:application