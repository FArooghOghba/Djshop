#!/bin/sh

set -e

echo "--> Waiting for db to be ready"
python -m src.manage wait_for_db

# Apply database migrations
echo "Apply database migrations"
python -m src.manage makemigration
python -m src.manage migrate

# Start server
echo "--> Starting web process"
python -m src.manage runserver 0.0.0.0:8000
