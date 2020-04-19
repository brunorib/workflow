#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py db migrate

# Apply database upgrades
echo "Apply database migrations"
python manage.py db upgrade

# Start server
echo "Starting server"
python manage.py run