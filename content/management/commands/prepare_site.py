"""
Gets the site ready every time the server starts:

    python manage.py prepare_site

It is safe to run again and again. It:
  1. updates the database tables (migrate),
  2. copies the images that come with the code into MEDIA_ROOT, if MEDIA_ROOT
     is somewhere else (for example a persistent disk), without overwriting,
  3. loads the starting content from WordPress, but only if the database is empty,
  4. creates an admin login from DJANGO_SUPERUSER_USERNAME / _EMAIL / _PASSWORD,
     but only if those are set and that user doesn't exist yet.
"""
import os
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from content.models import Service


class Command(BaseCommand):
    help = "Migrate, copy bundled images, load starting content once, create admin user."

    def handle(self, *args, **options):
        call_command("migrate", interactive=False, verbosity=1)
        self.copy_bundled_media()
        self.load_content_once()
        self.create_admin_once()

    def copy_bundled_media(self):
        source = Path(settings.BASE_DIR) / "media" / "uploads"
        target = Path(settings.MEDIA_ROOT) / "uploads"
        if not source.is_dir() or source.resolve() == target.resolve():
            return
        copied = 0
        for file in source.rglob("*"):
            if file.is_file() and file.suffix.lower() != ".php":
                dest = target / file.relative_to(source)
                if not dest.exists():
                    dest.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file, dest)
                    copied += 1
        self.stdout.write(f"Images copied to {target}: {copied}")

    def load_content_once(self):
        if Service.objects.exists():
            self.stdout.write("Content already in the database, not loading it again.")
            return
        call_command("loaddata", "initial_content")

    def create_admin_once(self):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not username or not password:
            return
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            return
        User.objects.create_superuser(
            username=username,
            email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
            password=password,
        )
        self.stdout.write(f"Admin user '{username}' created.")
