#!/bin/bash

# Apply database upgrades
echo "Apply database migrations"
python manage.py db upgrade

# Start server
echo "Starting server"
python manage.py run