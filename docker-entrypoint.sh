#!/bin/sh
set -e

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