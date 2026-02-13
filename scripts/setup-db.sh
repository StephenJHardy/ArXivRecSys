#!/bin/bash

# Exit on error
set -e

echo "Setting up ArXiv Recommendation System database..."

# Wait for PostgreSQL to be ready
echo "Waiting for PostgreSQL to be ready..."
until PGPASSWORD=postgres psql -h db -U postgres -c '\q' 2>/dev/null; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing database setup"

# Create database if it doesn't exist
PGPASSWORD=postgres psql -h db -U postgres -tc "SELECT 1 FROM pg_database WHERE datname = 'arxiv_recsys'" | grep -q 1 || \
    PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE arxiv_recsys"

# Run database migrations
cd /app
alembic upgrade head

echo "Database setup completed successfully!" 