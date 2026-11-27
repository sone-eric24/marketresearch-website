"""
Settings for the WS Market Research website.

Values that change between your computer and the live server are read from
environment variables (see .env.example). On your computer the defaults work
out of the box.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env_bool(name, default=False):
    return os.environ.get(name, str(default)).lower() in ("1", "true", "yes", "on")


def env_list(name, default=""):
    return [x.strip() for x in os.environ.get(name, default).split(",") if x.strip()]


# --- Security ---------------------------------------------------------------
DEBUG = env_bool("DJANGO_DEBUG", True)
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-insecure-key-change-me" if DEBUG else "",
)
if not SECRET_KEY:
    raise RuntimeError("Set the DJANGO_SECRET_KEY environment variable on the live server.")

ALLOWED_HOSTS = env_list(
    "DJANGO_ALLOWED_HOSTS",
    "localhost,127.0.0.1" if DEBUG else "ws-marketresearch.com,www.ws-marketresearch.com",
)
CSRF_TRUSTED_ORIGINS = env_list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "" if DEBUG else "https://ws-marketresearch.com,https://www.ws-marketresearch.com",
)

# Some hosts (Render, for example) tell the app its own address, like
# "my-site.onrender.com". If they do, allow it automatically so the site works
# before your own domain is connected.
for _host_var in ("RENDER_EXTERNAL_HOSTNAME", "EXTRA_ALLOWED_HOST"):
    _host = os.environ.get(_host_var, "").strip()
    if _host and _host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(_host)
        CSRF_TRUSTED_ORIGINS.append(f"https://{_host}")

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    # Off by default: on cPanel use Domains > "Force HTTPS Redirect" instead, which
    # avoids redirect loops behind the hosting proxy.
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SSL_REDIRECT", False)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24 * 30
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# --- Applications -------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # Serves CSS/images compressed and cached for a long time (fast on slow networks)
    "whitenoise.middleware.WhiteNoiseMiddleware",
    # Compresses HTML pages with gzip before sending them
    "django.middleware.gzip.GZipMiddleware",
    # Lets the browser reuse a page it already has (sends "304 Not Modified")
    "django.middleware.http.ConditionalGetMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "content.context_processors.site_info",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# --- Database -------------------------------------------------------------------
# SQLite is a single file and is plenty for a company website.
# On a host where the code folder is wiped at every deploy (Render, Docker),
# set DJANGO_DB_PATH to a file on a persistent disk, e.g. /var/data/db.sqlite3.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.environ.get("DJANGO_DB_PATH", BASE_DIR / "db.sqlite3"),
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- Language and time --------------------------------------------------------------
LANGUAGE_CODE = "en"
TIME_ZONE = "Africa/Douala"
USE_I18N = True
USE_TZ = True

# --- Static files (CSS) and media (uploaded images) ---------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": (
            "django.contrib.staticfiles.storage.StaticFilesStorage" if DEBUG
            else "whitenoise.storage.CompressedManifestStaticFilesStorage"
        ),
    },
}
MEDIA_URL = "/media/"
# Where uploaded images are kept. Like the database, point this at a persistent
# disk on hosts that wipe the code folder, e.g. DJANGO_MEDIA_ROOT=/var/data/media.
MEDIA_ROOT = Path(os.environ.get("DJANGO_MEDIA_ROOT", BASE_DIR / "media"))

# --- Email (contact form) -------------------------------------------------------------
# Messages are always saved in the admin. They are also emailed when SMTP is set.
CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "contact@ws-marketresearch.com")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "website@ws-marketresearch.com")
if os.environ.get("EMAIL_HOST"):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = os.environ["EMAIL_HOST"]
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT", "465"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER", "")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD", "")
    EMAIL_USE_SSL = EMAIL_PORT == 465
    EMAIL_USE_TLS = EMAIL_PORT == 587
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# --- Caching ----------------------------------------------------------------------------
# Pages are kept in memory for a few minutes so the server answers instantly.
CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
PAGE_CACHE_SECONDS = 0 if DEBUG else 60 * 10

# --- Company details used across the site ------------------------------------------------
SITE_INFO = {
    "name": "WS Market Research",
    "full_name": "Winning Solutions Market Research Firm",
    "tagline": "Unlock Cameroon’s Market Potential with Data-Driven Insights",
    "phone": "+237 655 747 721",
    "phone_link": "+237655747721",
    "whatsapp_link": "https://wa.me/237655747721",
    "email": "contact@ws-marketresearch.com",
    "address": "Jouvence, Yaoundé, Cameroon",
    "hours_week": "Monday to Friday: 7am – 7pm",
    "hours_weekend": "Weekend: 10am – 5pm",
    "linkedin": "https://www.linkedin.com/company/ws-market-research/",
    "facebook": "https://www.facebook.com/profile.php?id=100089710519932",
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "WARNING"},
}
