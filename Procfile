web: python manage.py collectstatic && python manage.py migrate && echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'duvan1997')" | python manage.py shell && gunicorn apptsinc.wsgi 