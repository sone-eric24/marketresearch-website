#!/usr/bin/env bash
# Runs once each time a new version of the site is built.
# Used by render.yaml; works the same on any Linux host.
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --noinput
