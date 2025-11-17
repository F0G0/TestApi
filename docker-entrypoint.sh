#!/usr/bin/env sh
set -e

echo "Waiting for database..."
python <<'PYCODE'
import os
import time

import psycopg2
from psycopg2 import OperationalError

host = os.environ.get("POSTGRES_HOST", "db")
port = os.environ.get("POSTGRES_PORT", "5432")
db = os.environ.get("POSTGRES_DB", "question_answers")
user = os.environ.get("POSTGRES_USER", "question_answers")
password = os.environ.get("POSTGRES_PASSWORD", "question_answers")

while True:
    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=db,
            user=user,
            password=password,
        )
        conn.close()
        break
    except OperationalError:
        print("Database unavailable, waiting 1s...")
        time.sleep(1)
PYCODE

python manage.py migrate --noinput
gunicorn TestApi.wsgi:application --bind 0.0.0.0:8000

