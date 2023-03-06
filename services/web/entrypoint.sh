#!/bin/sh

# Wait for the database to be ready
poetry run python /src/app/backend_pre_start.py

# Run the migrations
poetry run alembic upgrade head

# Seed the database
poetry run python /src/app/initial_data.py

mkdir -p -v /src/uploads/images/products
mkdir -p -v /src/uploads/images/slides

exec "$@"
