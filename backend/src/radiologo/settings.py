import os

import configparser
from datetime import timedelta

config = configparser.RawConfigParser()
if os.path.isfile("radiologo/resources/application.properties"):
    config.read("radiologo/resources/application.properties")
else:
    print("application.properties not found")
    exit(1)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = config.get("AppSettings", "SecretKey")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get("AppSettings", "Debug")

ALLOWED_HOSTS = []

BASE_FRONTEND_URL = "http://localhost:8080" if DEBUG else "https://radiologo.radiozero.pt"

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'programs',
    'users',
    'exceptions',
    'keys',
    'django_rest_passwordreset'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'radiologo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'radiologo/resources/emails_templates'),
                 os.path.join(BASE_DIR, 'radiologo/resources/keys_templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

KEYS_TEMPLATE_DIR = os.path.join(BASE_DIR, 'radiologo/resources/keys_templates/')
KEYDOC_MD = "keydoc.md"
FILE_UPLOAD_DIR = os.path.join(BASE_DIR, 'programs/uploaded/')

WSGI_APPLICATION = 'radiologo.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = config.get("AppSettings", "LanguageCode")
TIME_ZONE = config.get("AppSettings", "TimeZone")
USE_I18N = config.get("AppSettings", "UseI18N")
USE_L10N = config.get("AppSettings", "UseL10N")
USE_TZ = config.get("AppSettings", "UseTZ")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

# Email

EMAIL_HOST = config.get("Email", "EmailHost")
EMAIL_PORT = config.get("Email", "EmailPort")
EMAIL_USE_TLS = config.get("Email", "EmailTLS")

EMAIL_HOST_USER = config.get("Email", "EmailHostUser")
EMAIL_HOST_PASSWORD = config.get("Email", "EmailHostPassword")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_HTML = "invite_email.html"
EMAIL_TXT = "invite_email.txt"
PASSWORD_RESET_HTML = "password_reset.html"
PASSWORD_RESET_TXT = "password_reset.txt"
KEYDOC_HTML = "keydoc.html"
KEYDOC_TXT = "keydoc.txt"
UPLOAD_ACCEPT_TXT = "upload_accepted.txt"
UPLOAD_ACCEPT_HTML = "upload_accepted.html"
UPLOAD_REJECT_HTML = "upload_rejected.html"
UPLOAD_REJECT_TXT = "upload_rejected.txt"
UPLOAD_FAIL_HTML = "upload_failed.html"
UPLOAD_FAIL_TXT = "upload_failed.txt"
ADMIN_EMAIL = config.get("Email", "AdminEmail")

# Invite
INVITE_EXPIRY_DAYS = 7

# JWT
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Celery
CELERY_BROKER_URL='redis://redis:6379/0'

# Uploads
ARCHIVE_SERVER_IP = config.get("Servers", "ArchiveServer.ip")
ARCHIVE_SERVER_USERNAME = config.get("Servers", "ArchiveServer.username")
ARCHIVE_SERVER_PASSWORD = config.get("Servers", "ArchiveServer.password")
ARCHIVE_SERVER_UPLOAD_DIRECTORY = config.get("Servers", "ArchiveServer.rootUploadDirectory")
UPLOAD_SERVER_IP = config.get("Servers", "UploadServer.ip")
UPLOAD_SERVER_USERNAME = config.get("Servers", "UploadServer.username")
UPLOAD_SERVER_PASSWORD = config.get("Servers", "UploadServer.password")
UPLOAD_SERVER_UPLOAD_DIRECTORY = config.get("Servers", "UploadServer.rootUploadDirectory")
PLAYLIST_SERVER_IP = config.get("Servers", "PlaylistServer.ip")
PLAYLIST_SERVER_USERNAME = config.get("Servers", "PlaylistServer.username")
PLAYLIST_SERVER_PASSWORD = config.get("Servers", "PlaylistServer.password")
PLAYLIST_SERVER_UPLOAD_DIRECTORY = config.get("Servers", "PlaylistServer.rootUploadDirectory")