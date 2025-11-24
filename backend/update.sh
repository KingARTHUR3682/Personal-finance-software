#!/bin/bash

echo "Pulling from Github..."
git pull

./venv/bin/python manage.py migrate

./venv/bin/python manage.py collectstatic --noinput

echo "Rebooting Gunicorn Service..."
sudo systemctl restart gunicorn

echo "Finished！"