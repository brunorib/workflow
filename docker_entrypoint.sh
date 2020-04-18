#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
python manage.py db migrate

# Start server
echo "Starting server"
python manage.py run