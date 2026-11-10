from pathlib import Path
import environ
import os
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

# Initialize environment reading
env = environ.Env(DEBUG=(bool, True))  # Fallback to True if DEBUG is omitted locally

# Load local environment overrides when a development .env file is present.
environ.Env.read_env(BASE_DIR / ".env")


# SECURITY & ENVIRONMENT CONFIGURATION
SECRET_KEY = env("SECRET_KEY", default="dev-only-secret")
DEBUG = env("DEBUG")

# Handles parsing lists smoothly for local vs production hosts
# Production tip: On Render, add ".onrender.com" to your .env ALLOWED_HOSTS line.
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])



# CORE APPS & MIDDLEWARE
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "apps.dashboard",
    "apps.projects",
    "apps.content",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "PortfolioSite.urls"

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
            ]
        },
    }
]

WSGI_APPLICATION = "PortfolioSite.wsgi.application"


# DATABASE CONFIGURATION (DOCKER / SQLITE LOCAL VS PRODUCTION POSTGRES)
# fallback to using a local development SQLite if DATABASE_URL is not found.
DATABASES = {
    "default": env.db("DATABASE_URL", default=f'sqlite:///{BASE_DIR / "db.sqlite3"}')
}

# secure SSL layers to handle inbound pipeline queries in production.
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
    }
    # Dynamic persistent connection pools (keeps live container fast)
    DATABASES["default"]["CONN_MAX_AGE"] = 600


# PASSWORDS & LOCALIZATION
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# STATIC & MEDIA FILE ASSET HANDLING
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# WhiteNoise production assets optimizations
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"



# TRANSACTIONAL MAILING CONFIGURATIONS
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default="portfolio@example.com")
CONTACT_EMAIL = env("CONTACT_EMAIL", default=DEFAULT_FROM_EMAIL)


# DRF & OPENAPI INTERACTIVE DOCUMENTATION (SPECTACULAR)
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "PortfolioSite API",
    "DESCRIPTION": "Public API for portfolio content, projects, and system health.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
