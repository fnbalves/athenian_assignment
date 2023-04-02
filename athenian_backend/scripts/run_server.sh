#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python -m uvicorn athenian_backend.asgi:application