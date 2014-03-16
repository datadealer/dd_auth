# Django settings for dd_auth project.
import os
from django.utils.translation import ugettext_lazy as _
APP_PATH = os.path.dirname(os.path.abspath(__file__))

DEBUG = False
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/dd_auth.db' % APP_PATH,     # Or path to database file if using sqlite3.
        'USER': '',                             # Not used with sqlite3.
        'PASSWORD': '',                         # Not used with sqlite3.
        'HOST': '',                             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Vienna'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


LANGUAGES = (
    ('de', _('German')),
    ('en', _('English')),
)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '%s/../static' % APP_PATH

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/dd_auth_static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '6g^74v__c=-!$e6qiqw1c53is2*y*4ayl#is)btc7w!i45tRXs'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dd_auth.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'dd_auth.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/%s/templates' % APP_PATH,
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    'allauth.account.context_processors.account',
    'allauth.socialaccount.context_processors.socialaccount',
    'django.core.context_processors.i18n'
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jsonrpc',
    'south',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.github',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.openid',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.soundcloud',
    #'allauth.socialaccount.providers.twitter',
    'django.contrib.admin',
    'dd_auth.dd_user_sync',
    'dd_auth.dd_djangomessage_null',
    'dd_invitation',
    'django_extensions',
)

# django.contrib.messages storage

MESSAGE_STORAGE = 'dd_auth.dd_djangomessage_null.storage.NullStorage'

# Password hashers

PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.BCryptPasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

EMAIL_HOST='some.mail.host'
EMAIL_PORT=25
EMAIL_HOST_USER='username'
EMAIL_HOST_PASSWORD='secret'
EMAIL_USE_TLS=True

DEFAULT_FROM_EMAIL=SERVER_EMAIL='robot@datadealer.com'

LOGIN_REDIRECT_URL='/#load'
#LOGIN_REDIRECT_URLNAME='https://datadealer.com/#load'

ACCOUNT_LOGOUT_ON_GET=True
ACCOUNT_LOGOUT_REDIRECT_URL='/'

### REDIS SESSIONS

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0
#SESSION_REDIS_PASSWORD = 'password'
SESSION_REDIS_PREFIX = 'dd_session'

INVITATION_REQUIRED = True
INVITATION_FAILED = '%s%s' % (ACCOUNT_LOGOUT_REDIRECT_URL, '#access_denied')


# Needed for allauth email authentication

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

### ALLAUTH SETTINGS
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
#ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL='/some/url' # after email confirmation, anonymous
#ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL='/some/url' # after email confirmation, logged in
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 5
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'
ACCOUNT_EMAIL_SUBJECT_PREFIX = "[Data Dealer] "
#ACCOUNT_SIGNUP_FORM_CLASS
ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True # password twice
ACCOUNT_UNIQUE_EMAIL = True # ensure email uniqueness
#ACCOUNT_USER_DISPLAY (=a callable returning user.username)
ACCOUNT_USERNAME_MIN_LENGTH = 4
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_PASSWORD_INPUT_RENDER_VALUE = False
ACCOUNT_PASSWORD_MIN_LENGTH = 8
ACCOUNT_ADAPTER = "dd_auth.adapters.DDAccountAdapter"
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_AVATAR_SUPPORT = False
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'oauth2' ,
        'LOCALE_FUNC': lambda request:'en_US'
    },
    'google': {
        'SCOPE': [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'
        ],
    },
    'linkedin': {
        'SCOPE': ['r_emailaddress'],
    },
    'persona': {
        'REQUEST_PARAMETERS': {'siteName': 'Data Dealer' },
    },
}

RPC4DJANGO_RESTRICT_XMLRPC=True

DD_MONGO_DB = {
    'host': 'localhost',
    'port': 27017,
    'max_pool_size': 32,
    'db': 'somedb',
    'users_collection': 'users'
}

# Serve static files through django?
DD_SERVE_STATIC = False

ALLOWED_HOSTS = ['.datadealer.net', 'datadealer']

if DEBUG == True:
  EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
  EMAIL_FILE_PATH = '/tmp/dd_auth/mail'

try:
    from dd_auth.settings_local import *
except ImportError:
    pass
