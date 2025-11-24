#!/bin/bash

echo "Pulling from Github..."
git pull

echo "Installing Requirements..."
./venv/bin/pip install -r requirements.txt

./venv/bin/python manage.py migrate

./venv/bin/python manage.py collectstatic --noinput

echo "Rebooting Gunicorn Service..."
sudo systemctl restart gunicorn

echo "Finished！"