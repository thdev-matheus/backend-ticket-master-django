"""
Django settings for _project project.

Generated by 'django-admin startproject' using Django 3.2.15.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
import dotenv

dotenv.load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# descomentar quando colocar em produção
# ALLOWED_HOSTS = ["url_do_app_no_deploy", "localhost"]
ALLOWED_HOSTS = []


# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PART_APPS = [
    "rest_framework",
    "rest_framework.authtoken",  # ou jwt
    "drf_spectacular",
]

MY_APPS = [
    "users",
    "comments",
    "departments",
    "tickets",
    "solutions",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PART_APPS + MY_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "_project.urls"

TEMPLATES = [
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

WSGI_APPLICATION = "_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Se tiver uma chave SQLITE no .env executa o banco de dados do sqlite. Senão se tiver uma chave OPERATION executa o postgres que está no container direto do contexto local(para executar comandos de terminal direcionados ao container sem precisar entrar no container). senão aciona o banco normalmente do container. qualquer dúvida só chamar.
# if os.environ.get("SQLITE"):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.sqlite3",
#             "NAME": BASE_DIR / "db.sqlite3",
#         }
#     }
# elif os.environ.get("OPERATION"):
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.environ.get("POSTGRES_DB"),
#             "USER": os.environ.get("POSTGRES_USER"),
#             "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#             "HOST": "localhost",
#             "PORT": 5050,
#         }
#     }
# else:
#     DATABASES = {
#         "default": {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": os.environ.get("POSTGRES_DB"),
#             "USER": os.environ.get("POSTGRES_USER"),
#             "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
#             "HOST": os.environ.get("POSTGRES_HOST"),
#             "PORT": os.environ.get("PORT"),
#         }
#     }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# Config do rest_framework
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# Config da Documentação
SPECTACULAR_SETTINGS = {
    "TITLE": "Ticket Master",
    "DESCRIPTION": "Esta API foi criada para a entrega do projeto final do M5",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

DATABASE_URL = os.getenv(
    "DATABASE_URL"
)  # url do banco de dados. quando for feito o deploy da api essa config vai cuidar de linkar um com o outro. A chave no .env é gerada automaticamente no deploy quando setamos o add-on do postgres no heroku

if (
    DATABASE_URL
):  # se a variável estiver setada no .env executa as modificações no campo database para a produção
    db_from_env = dj_database_url.config(
        default=DATABASE_URL,
        conn_max_age=500,
        ssl_require=True,
    )
    DATABASES["default"].update(db_from_env)
    DEBUG = False  # seta o debug pra False quando estiver em produção