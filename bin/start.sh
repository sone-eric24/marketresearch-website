#!/usr/bin/env bash
# Starts the website. Used by render.yaml, the Procfile and the Dockerfile.
set -o errexit

# Make sure the folders for the database and images exist (e.g. on a disk).
if [ -n "$DJANGO_DB_PATH" ]; then mkdir -p "$(dirname "$DJANGO_DB_PATH")"; fi
if [ -n "$DJANGO_MEDIA_ROOT" ]; then mkdir -p "$DJANGO_MEDIA_ROOT"; fi

# Update the database, copy images, load content the first time.
python manage.py prepare_site

# Start the real web server. $PORT is given by the host (Render, Railway, ...).
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-2}" \
  --timeout 60 \
  --access-logfile -
