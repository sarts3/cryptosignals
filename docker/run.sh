#!/bin/sh

python3 manage.py migrate
cp scripts/create_fixtures.py .
python3 create_fixtures.py
python3 manage.py loaddata fixtures/initial_data.json

crond &
python3 manage.py runserver 0.0.0.0:8000

