#!/bin/bash

python3 manage.py makemigrations
python3 manage.py migrate
python -m uvicorn --host 0.0.0.0 athenian_backend.asgi:application