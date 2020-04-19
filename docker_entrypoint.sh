#!/bin/bash

mkdir -p /app/migrations/versions

# Apply database upgrades
echo "Apply database migrations"
python manage.py db migrate

# Start server
echo "Starting server"
python manage.py run