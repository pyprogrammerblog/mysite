# mysite

Personal Blog:

1. git clone https://github.com/pyprogrammerblog/mysite
2. virtualenv -p python3 .
3. pip install -r requirements.txt
4. python3 manage.py collectstatics
5. python3 manage.py migrate
6. python3 manage.py runserver

Locally, in order to run redis for celery:

7. celery --app=mysite.celery:app worker --loglevel=INFO
8. celery -A mysite beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
