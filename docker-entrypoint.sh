#!/bin/sh
#!/bin/bash
set -e

if [ "$SERVICE_ROLE" = "web" ]; then
    echo ">> Применяю миграции..."
    python manage.py migrate --noinput

    echo ">> Собираю статику..."
    python manage.py collectstatic --noinput

    echo ">> Запускаю gunicorn..."
    exec gunicorn config.wsgi:application \
        --bind 0.0.0.0:8000 \
        --workers 3 \
        --timeout 60 \
        --access-logfile - \
        --error-logfile -

elif [ "$SERVICE_ROLE" = "celery" ]; then
    echo ">> Запускаю celery worker..."
    exec celery -A config worker --loglevel=info

else
    echo "ERROR: SERVICE_ROLE не задан (ожидается 'web' или 'celery')"
    exit 1
fi