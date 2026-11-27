# Lets the site run on any host that accepts Docker (Fly.io, Koyeb, a VPS, ...).
# Render doesn't need this file: it uses render.yaml instead.
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_DEBUG=False \
    DJANGO_DB_PATH=/data/db.sqlite3 \
    DJANGO_MEDIA_ROOT=/data/media \
    PORT=8000

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# collectstatic needs a secret key to start Django; this one is only for the build.
RUN DJANGO_SECRET_KEY=build-only python manage.py collectstatic --noinput

# Keep the database and uploaded images here; mount a volume on /data.
VOLUME /data
EXPOSE 8000
CMD ["bash", "bin/start.sh"]
