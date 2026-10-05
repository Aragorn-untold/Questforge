#!/usr/bin/env bash
set -o errexit

pip install -r requirements

python manage.py collectstatic --no-input

python manage.py migrate
