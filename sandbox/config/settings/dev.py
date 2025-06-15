"""
Django settings for your project.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.2/ref/settings/
"""

import os
from pathlib import Path
from typing import Any

import structlog
from environs import env

# =========================================================================
# PATH CONFIGURATION
# =========================================================================

CONFIG_PATH = Path(__file__)
BASE_DIR = CONFIG_PATH.parent.parent.parent
ROOT_DIR = BASE_DIR.parent

# =========================================================================
# ENVIRONMENT SETTINGS
# =========================================================================

env_file = f"{ROOT_DIR}/.env.test"

if os.path.isfile(env_file):
    env.read_env(env_file, recurse=False)
else:
    env.read_env()

CURRENT_ENV = env.str("DJANGO_SETTINGS_MODULE").split(".")[-1]

# =========================================================================
# CORE SETTINGS
# =========================================================================
SECRET_KEY = "this-is-a-mock-secret-key"

DEBUG = True
TEST = False

ALLOWED_HOSTS = ["*"]
SERVER_URL = env.str("SERVER_URL", "http://localhost:8000")

# =========================================================================
# APPLICATION DEFINITION
# =========================================================================

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "django_cleanup.apps.CleanupConfig",
    "debug_toolbar",
    "django_extensions",
    "drf_spectacular_extras",
    "dummy",
]

# =========================================================================
# MIDDLEWARE CONFIGURATION
# =========================================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django_structlog.middlewares.RequestMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware"
]

# =========================================================================
# URL CONFIGURATION
# =========================================================================

ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# =========================================================================
# TEMPLATE CONFIGURATION
# =========================================================================

TEMPLATES: list[dict[str, Any]] = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# =========================================================================
# DATABASE CONFIGURATION
# =========================================================================
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.str("POSTGRES_DB", ""),
        "USER": env.str("POSTGRES_USER", ""),
        "PASSWORD": env.str("POSTGRES_PASSWORD", ""),
        "HOST": env.str("POSTGRES_HOST", "localhost"),
        "PORT": env.int("POSTGRES_PORT", 5432),
        "OPTIONS": {
            "pool": True,
        },
    }
}

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



# =========================================================================
# AUTHENTICATION CONFIGURATION
# =========================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =========================================================================
# INTERNATIONALIZATION
# =========================================================================

LANGUAGE_CODE = "en"

TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =========================================================================
# STATIC FILES CONFIGURATION
# =========================================================================

STATIC_ROOT = str(BASE_DIR / "static")
STATIC_URL = "static/"

MEDIA_ROOT = str(BASE_DIR / "media/")
MEDIA_URL = "media/"

# =========================================================================
# REST FRAMEWORK CONFIGURATION
# =========================================================================
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PARSER_CLASSES": (
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "PAGE_SIZE": 20,
}

# =========================================================================
# API DOCUMENTATION CONFIGURATION
# =========================================================================

SPECTACULAR_SETTINGS: dict[str, Any] = {
    "TITLE": "",
    "DESCRIPTION": "DRF Spectacular Extras OpenAPI specification",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "COMPONENT_SPLIT_REQUEST": True,
    "COMPONENT_NO_READ_ONLY_REQUIRED": True,
    "SCHEMA_COERCE_PATH_PK_SUFFIX": True,
    "DISABLE_ERRORS_AND_WARNINGS": False if CURRENT_ENV == "dev" else True,
    "SERVE_PERMISSIONS": [],
    "SERVE_AUTHENTICATION": [],

}

# =========================================================================
# CORS CONFIGURATION
# =========================================================================

CORS_ALLOWED_ORIGINS: list[str] = env.list("CORS_ALLOWED_ORIGINS", default=[])
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[SERVER_URL])

# =========================================================================
# LOGGING CONFIGURATION
# =========================================================================

pre_chain = [
    structlog.contextvars.merge_contextvars,
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.stdlib.add_logger_name,
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
]

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": (
                [
                    structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                    structlog.dev.ConsoleRenderer(
                        exception_formatter=structlog.dev.plain_traceback
                    ),
                ]
            ),
            "foreign_pre_chain": pre_chain,
        },
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processors": [
                structlog.processors.dict_tracebacks,
                structlog.stdlib.ProcessorFormatter.remove_processors_meta,
                structlog.processors.JSONRenderer(),
            ],
            "foreign_pre_chain": pre_chain,
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "plain_console",
        }
    },
    "loggers": {
        "": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "django_structlog": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "django_structlog_drf_spectacular_extras": {
            "handlers": ["console"],
            "level": "INFO",
        },
        "drf_spectacular_extras": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}

structlog.configure(
    processors=pre_chain  # type: ignore[arg-type]
    + [
        structlog.stdlib.filter_by_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

# =========================================================================
# DJANGO SHELL_PLUS
# =========================================================================
SHELL_PLUS = "ipython"
IPYTHON_ARGUMENTS = [
    "--ext",
    "autoreload",
]
