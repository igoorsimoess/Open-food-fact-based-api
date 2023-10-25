#!/bin/bash

# Apply database migrations
python manage.py migrate
sleep 2

# Run your custom Python script
python db_connection.py

# Start your Django application
sleep 2
exec python manage.py runserver 0.0.0.0:8000
