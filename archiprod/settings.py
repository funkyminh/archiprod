# Django settings for archiprod project.
import os
import sys
from os.path import dirname, abspath

from django.utils.translation import ugettext as _

PROJECT_DIR = abspath(dirname(__file__))
SITE_DIR = os.path.dirname(PROJECT_DIR)


DEBUG = bool(os.environ.get('DEBUG', False))
TEMPLATE_DEBUG = DEBUG
TESTING = 'test' in sys.argv

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')  #'smtp.ircam.fr' set to smarthost.ircam.fr pour la prod.
EMAIL_PORT = os.environ.get('EMAIL_PORT', '1025') # for ircam 25


FILE_UPLOAD_HANDLERS = (
    "progressbarupload.uploadhandler.ProgressBarUploadHandler",
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

ADMINS = (
    ('Samuel Goldszmidt', 'samuel.goldszmidt@ircam.fr'),
    ('Minh Dang', 'minh.dang@ircam.fr'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.%s' % os.environ.get('DATABASE_ENGINE', 'mysql'),  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': os.environ.get('DATABASE_NAME'),                      # Or path to database file if using sqlite3.
        'USER': os.environ.get('DATABASE_USER'),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': os.environ.get('DATABASE_HOST', ''),                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': os.environ.get('DATABASE_PORT', ''),                      #
    },
    'acanthes': {
        'ENGINE': 'django.db.backends.%s' %  os.environ.get('DATABASE_ENGINE', 'mysql'),  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'acanthes_db',                      # Or path to database file if using sqlite3.
        'USER': os.environ.get('DATABASE_USER'),                      # Not used with sqlite3.
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),                  # Not used with sqlite3.
        'HOST': os.environ.get('DATABASE_HOST', ''),                    # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

if os.environ.get('DATABASE_ENGINE', None) == None:
    DATABASES['default']['OPTIONS'] = {"init_command": "SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci", }

DATABASE_ROUTERS = ['archiprod.router.AcanthesRouter', ]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

gettext = lambda s: s

LANGUAGES = (
    ('fr', gettext('French')),
    ('en', gettext('English')),
)

LOCALE_PATHS = (
    'archiprod/locale',
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


MEDIA_ROOT = os.environ.get('MEDIA_ROOT', os.path.join(SITE_DIR, 'media'))
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')

STATIC_ROOT = os.environ.get('STATIC_ROOT', os.path.join(SITE_DIR, 'static'))
STATIC_URL = os.environ.get('STATIC_URL', '/static/')

STREAM_ROOT = os.environ.get('STREAM_ROOT', os.path.join(SITE_DIR, 'stream'))
STREAM_URL = os.environ.get('STREAM_URL', '/stream/')


OLD_ARCHIVES_VIDEO = "old_archives/video/"
OLD_ARCHIVES_AUDIO = "old_archives/audio/"
OLD_PROGRAM_NOTE = "old_archives/programnote/"

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
    'compressor.finders.CompressorFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY')

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'utils.middleware.SetRemoteAddrFromForwardedFor',
    'utils.middleware.SetUserLocationFromAddr',
    #'django.middleware.locale.LocaleMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "archiprod.context_processors.is_archiprod",
    "archiprod.context_processors.in_situ",
    "archiprod.context_processors.site"
)

ROOT_URLCONF = 'archiprod.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'archiprod.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_DIR, 'templates')
)

AUTHENTICATION_BACKENDS = (
    'utils.backends.CustomIMAPBackend',
    'django.contrib.auth.backends.ModelBackend',
)

IMAPAUTH_HOST = 'imap.ircam.fr'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'ressources',
    'south',
    'old',
    'django_extensions',
    'mptt',
    'archives',
    'utils',
    'events',
    'progressbarupload',
    'feincms',
    'django_rq',
    'django_rq_dashboard',
    'haystack',
    'compressor',
    'autocomplete_light',
    'rosetta'
)

REDIS_URL = os.environ.get('REDIS_URL', 'localhost:6379').split(':')

RQ_QUEUES = {
    'default': {
        'HOST': REDIS_URL[0],
        'PORT': int(REDIS_URL[1]),
        'DB': 0,
    },
    'archive': {
        'HOST': REDIS_URL[0],
        'PORT': int(REDIS_URL[1]),
        'DB': 0,
    }
}

if DEBUG:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'recess {infile} --compile > {outfile}'),
    )
else:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter']
COMPRESS_JS_FILTERS = []


HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
        'URL': os.environ.get('SOLR_URL', 'http://127.0.0.1:8983/solr/dev')
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

SOUTH_TESTS_MIGRATE = False
SKIP_SOUTH_TESTS = True

RQ_SHOW_ADMIN_LINK = True

FTP_ROOT = os.environ.get('FTP_ROOT', '/srv/archiprod/ftp')

FILE_UPLOAD_TEMP_DIR = os.environ.get('TMP_ROOT', '/srv/archiprod/tmp')


if DEBUG:
    TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'
    COVERAGE_REPORT_HTML_OUTPUT_DIR = os.path.join(SITE_DIR, 'coverage')
    COVERAGE_MODULE_EXCLUDES = ['tests$', 'settings$', 'urls$', 'locale$',
                                'common.views.test', '__init__', 'django',
                                'migrations', 'acanthes']
