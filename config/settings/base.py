

from datetime import timedelta
import os
from pathlib import Path
import environ
import firebase_admin
from firebase_admin import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


APPS_DIR = BASE_DIR/'applications'

env = environ.Env()

environ.Env.read_env(BASE_DIR/'.env')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY=env('SECRET_KEY')


ALLOWED_HOSTS = []

CORS_ORIGIN_ALLOW_ALL = True

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'django_filters',
    'corsheaders',
    "fcm_django",
    'import_export',
    
    'django_celery_beat',
    'django_celery_results',
]


USER_MS = [
    'applications.users.apps.UsersConfig',
]

HISTORY_MS = [
    'applications.history.apps.HistoryConfig',
]

INSPECTIONS_MS = [
    'applications.inspections.apps.InspectionsConfig',
]

OBSERVATIONS_MS = [
    'applications.observations.apps.ObservationsConfig',
]


SERVICES_APPS = USER_MS + HISTORY_MS + INSPECTIONS_MS + OBSERVATIONS_MS

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + SERVICES_APPS

# FCM firebase
""" FCM_DJANGO_SETTINGS = {
     # default: _('FCM Django')
    "APP_VERBOSE_NAME": "FCM_Django",
    "FCM_SERVER_KEY": "AAAAbET7T30:APA91bEwykuj7185eUhyAUZ6bWxPczNkYU-5VRVnjc_-AFDY9276clTkxP3CichfLUXbdBDula3nP5o9twSQbWzs1_j5WBwV1s2K2yua6xdBeR8PGFh4WoWbJ2sMra978hLd8zHWdwb5",
     # true if you want to have only one active device per registered user at a time
     # default: False
    "ONE_DEVICE_PER_USER": False,
     # devices to which notifications cannot be sent,
     # are deleted upon receiving error response from FCM
     # default: False
    "DELETE_INACTIVE_DEVICES": False,
    # Transform create of an existing Device (based on registration id) into
                # an update. See the section
    # "Update of device with duplicate registration ID" for more details.
    "UPDATE_ON_DUPLICATE_REG_ID": True,
}
cred = credentials.Certificate(os.path.join(BASE_DIR, 'credentials.json'))
firebase_admin.initialize_app(cred) """

# Middleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

# CACHE
""" CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
} """

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(hours=24),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'



# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'es-pe'

TIME_ZONE = 'America/Lima'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# CELERY
CELERY_BROKER_URL = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_TRACK_STARTED = True
CELERY_IGNORE_RESULT = False

""" CELERY_BEAT_SCHEDULE = {
    "scheduled_task": {
        "task": "applications.assistance.tasks.test_function",
        "schedule": 10.00
    }
} """