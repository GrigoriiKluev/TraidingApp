#!/bin/bash

alembic revision --autogenerate -m "create all tables"
alembic upgrade head

cd src

gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000