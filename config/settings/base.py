# -*- coding: utf-8 -*-
"""
Django settings for gglobal project.

For more information on this file, see
https://docs.djangoproject.com/en/dev/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/dev/ref/settings/
"""
from __future__ import absolute_import, unicode_literals

import environ
from django.utils.translation import ugettext_lazy as _


ROOT_DIR = environ.Path(__file__) - 3  # (gglobal/config/settings/base.py - 3 = gglobal/)
APPS_DIR = ROOT_DIR.path('gglobal')

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# .env file, should load only in development environment
READ_DOT_ENV_FILE = env.bool('DJANGO_READ_DOT_ENV_FILE', default=False)

if READ_DOT_ENV_FILE:
    # Operating System Environment variables have precedence over variables defined in the .env file,
    # that is to say variables from the .env files will only be used if not defined
    # as environment variables.
    env_file = str(ROOT_DIR.path('.env'))
    print('Loading : {}'.format(env_file))
    env.read_env(env_file)
    print('The .env file has been loaded. See base.py for more information')

# APP CONFIGURATION
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'django.contrib.sitemaps',
    # Useful template tags:
    # 'django.contrib.humanize',

    # Admin
    'django.contrib.admin',
    #'django.contrib.admin.apps.SimpleAdminConfig',
]
THIRD_PARTY_APPS = [
    'crispy_forms',  # Form layouts
    
    # Enable allauth.
    'allauth',  # registration
    'allauth.account',  # registration
    'allauth.socialaccount',  # registration
    
    'hitcount', # qa needed
    'markdownx', # qa needed
    'taggit', # qa needed
    'annoying', # AutoOneToOneField
    'turbolinks', # Turbolinks

    #'cities', # Django-cities
    'cities_light', # Django-cities-light

    'ckeditor', # CKEditor

    'categories', # Django-categories
    'categories.editor', # Django-categories
    'mptt',
    
    "geoposition", # Django-geoposition

    'wagtail.wagtailcore',
    'wagtail.wagtailadmin',
    'wagtail.wagtailforms',
    'wagtail.wagtailredirects',
    'wagtail.wagtailembeds',
    'wagtail.wagtailsites',
    'wagtail.wagtailusers',
    'wagtail.wagtailsnippets',
    'wagtail.wagtaildocs',
    'wagtail.wagtailimages',
    'wagtail.wagtailsearch',


    'wagtail.contrib.wagtailstyleguide',
    'wagtail.contrib.modeladmin',
    'experiments',
    'wagtailmetadata',
    'meta',
    'flags',
    'wagtail.contrib.wagtailsitemaps',
    'wagtail.contrib.settings',
    'wagtailsurveys',

    'wagtailfontawesome',
    'wagtailmenus',
    'wagtailblocks_cards',
    'wagtailgridder',

    'mapwidgets',
    # django-viewflow and django-material
    #'viewflow',
    'material.theme.blue', 
    'material', # django-material
    'material.frontend',
    'gglobal.viewflow.frontend',
    #####################################

    'notifications', # django-notifications
    
    #'djcelery', 
    'django_celery_results',
    'django_celery_beat',
    'django_celery_monitor',

    'request', # django-request
    #'cacheops', # django-cacheops
    'cachalot',
    #'ajax_select',
    'django_feedparser', # django-feedparser
    'controlcenter', # django-controllcenter
    'avatar', # django-avatar http://django-avatar.readthedocs.io/en/latest/
    'dashing', # django-dashing https://github.com/talpor/django-dashing
    'djmoney', # django-money https://github.com/django-money/django-money
    'djmoney_rates', # django-money-rates https://github.com/evonove/django-money-rates
]

# Apps specific for this project go here.
LOCAL_APPS = [
    # custom users app
    'gglobal.users.apps.UsersConfig',
    # Your stuff: custom apps go here
    'gglobal.qa.apps.QAConfig',
    'gglobal.cms.apps.CMSConfig',
    'gglobal.crm.apps.CRMConfig',
    'gglobal.service.apps.ServiceConfig',
    'gglobal.viewflow.apps.ViewflowConfig', # django-viewflow
    'gglobal.city.apps.CityConfig',

]

PRE_DJANGO_APPS = [
    'dal', # autocomplete light v.3
    'dal_select2', # autocomplete light v.3
    'dal_queryset_sequence', # autocomplete light v.3
    'jet.dashboard',
    'jet', # Django-JET
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = PRE_DJANGO_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIDDLEWARE CONFIGURATION
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'request.middleware.RequestMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'wagtail.wagtailcore.middleware.SiteMiddleware',
    'wagtail.wagtailredirects.middleware.RedirectMiddleware',
    #'wagtailthemes.middleware.ThemeMiddleware',
    'turbolinks.middleware.TurbolinksMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
]

# MIGRATIONS CONFIGURATION
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {
    'sites': 'gglobal.contrib.sites.migrations'
}

# DEBUG
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool('DJANGO_DEBUG', False)

# FIXTURE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    str(APPS_DIR.path('fixtures')),
)

# EMAIL CONFIGURATION
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env('DJANGO_EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')

# MANAGER CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("""Narnik Gamarnik""", 'narnikgamarnikus@gmail.com'),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# DATABASE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': env.db('DATABASE_URL', default='postgres:///gglobal'),
}

DATABASES['default']['ATOMIC_REQUESTS'] = True


# GENERAL CONFIGURATION
# ------------------------------------------------------------------------------
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Minsk'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'ru-RU'
LANGUAGES = [
    ('ru', _('Russian')),
]

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# TEMPLATE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
        'DIRS': [
            str(APPS_DIR.path('templates')),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                # 'wagtailthemes.loaders.ThemeLoader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.csrf',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                # Your stuff: custom template context processors go here
                'wagtail.contrib.settings.context_processors.settings',
                'wagtailmenus.context_processors.wagtailmenus',
            ],
        },
    },
]

# See: http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR('media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'

# URL Configuration
# ------------------------------------------------------------------------------
ROOT_URLCONF = 'config.urls'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'config.wsgi.application'

# PASSWORD STORAGE SETTINGS
# ------------------------------------------------------------------------------
# See https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
]

# PASSWORD VALIDATION
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
# ------------------------------------------------------------------------------

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

# AUTHENTICATION CONFIGURATION
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Some really nice defaults
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_EMAIL_VERIFICATION = 'optional'#'mandatory'

ACCOUNT_ALLOW_REGISTRATION = env.bool('DJANGO_ACCOUNT_ALLOW_REGISTRATION', True)
ACCOUNT_ADAPTER = 'gglobal.users.adapters.AccountAdapter'
SOCIALACCOUNT_ADAPTER = 'gglobal.users.adapters.SocialAccountAdapter'



# ALLAUTH SETTINGS #
ACCOUNT_FORMS = {
    "login": "gglobal.users.forms.CustomLoginForm",
    #"signup": "gglobal.users.forms.CustomSignupForm",
    "confirm-email": "gglobal.users.forms.CustomSignupForm",
}
ACCOUNT_USERNAME_MIN_LENGTH = 1
ACCOUNT_SIGNUP_FORM_CLASS = None
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = None
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'account_login'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

# Custom user app defaults
# Select the correct user model
AUTH_USER_MODEL = 'users.User'
#LOGIN_REDIRECT_URL = 'users:redirect'
LOGIN_URL = 'account_login'

MASTER_HOME_URL = '/кабинет'

# SLUGLIFIER
AUTOSLUG_SLUGIFY_FUNCTION = 'slugify.slugify'

########## CELERY
INSTALLED_APPS += ['gglobal.taskapp.celery.CeleryConfig']
BROKER_URL = env('CELERY_BROKER_URL', default='django://')
if BROKER_URL == 'django://':
    CELERY_RESULT_BACKEND = 'redis://'
else:
    CELERY_RESULT_BACKEND = BROKER_URL
########## END CELERY
# django-compressor
# ------------------------------------------------------------------------------
INSTALLED_APPS += ['compressor']
STATICFILES_FINDERS += ['compressor.finders.CompressorFinder']

# Location of root django.contrib.admin URL, use {% url 'admin:index' %}
ADMIN_URL = r'^admin/'

# Your common stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------

# django-wagtail
# ------------------------------------------------------------------------------
WAGTAIL_SITE_NAME = 'ремонт-пк-и-ноутбуков.бел'
WAGTAIL_USAGE_COUNT_ENABLED = True

#GOOGLE_MAP_API_KEY = 'AIzaSyAUYmoNhNMy-DMjKLIbLdjlidm1qVscuoA'
GOOGLE_MAP_API_KEY = 'AIzaSyBO-_WYrcSrU79tLuKPiINGkCJ1e__RWWw'
# django-cities
# ------------------------------------------------------------------------------
CITIES_FILES = {
    # ...
    'city': {
       'filename': "BY.zip",
       'urls':      ['http://download.geonames.org/export/dump/'+'{filename}']
    },
    # ...
}
CITIES_POSTAL_CODES = ['BY']

CITIES_LOCALES = ['ru', 'LANGUAGES']

# django-cities-light
# ------------------------------------------------------------------------------
CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru']
CITIES_LIGHT_INCLUDE_COUNTRIES = ['BY']
CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG', 'PPLL', 'PPLR', 'PPLS', 'STLMT',]


# django-geoposition
# ------------------------------------------------------------------------------
GEOPOSITION_GOOGLE_MAPS_API_KEY = GOOGLE_MAP_API_KEY

GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
}

GEOPOSITION_MARKER_OPTIONS = {
    'cursor': 'move'
}


# CKEDITOR SETTINGS
# ------------------------------------------------------------------------------

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Basic',
        'height': 300,
        'width': '100%',
    },
}

CKEDITOR_JQUERY_URL = 'https://ajax.googleapis.com/ajax/libs/jquery/2.2.4/jquery.min.js'

CATEGORIES_SETTINGS = {
    'ALLOW_SLUG_CHANGE': True
}


# CACHEOPS SETTINGS
# ------------------------------------------------------------------------------
'''
CACHEOPS_REDIS = {
    'host': 'localhost', # redis-server is on same machine
    'port': 6379,        # default redis port
    'db': 1,             # SELECT non-default redis database
                         # using separate redis db or redis instance
                         # is highly recommended

    'socket_timeout': 3,   # connection timeout in seconds, optional
    #'password': '...',     # optional
    #'unix_socket_path': '' # replaces host and port
}

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This includes request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},
    'users.user': {'ops': 'get', 'timeout': 60},
    'cities_light.city': {'ops': 'get', 'timeout': 60*60*30},
    'cities_light.country': {'ops': 'get', 'timeout': 60*60*30},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': ('fetch', 'get'), 'timeout': 60*60},

    # Cache gets, fetches, counts and exists to Permission
    # 'all' is just an alias for ('get', 'fetch', 'count', 'exists')
    'auth.permission': {'ops': 'all', 'timeout': 60*60},

    # Enable manual caching on all other models with default timeout of an hour
    # Use Post.objects.cache().get(...)
    #  or Tags.objects.filter(...).order_by(...).cache()
    # to cache particular ORM request.
    # Invalidation is still automatic
    '*.*': {'ops': (), 'timeout': 60*5},

    # And since ops is empty by default you can rewrite last line as:
    '*.*': {'timeout': 60*5},
}

CACHEOPS_DEGRADE_ON_FAILURE = True
'''

CACHALOT_ENABLED = True
CACHALOT_TIMEOUT = None
CACHALOT_CACHE_RANDOM = False
CACHALOT_INVALIDATE_RAW = True
#CACHALOT_ONLY_CACHABLE_TABLES = frozenset()

'''
# AJAX_LOOKUP SETTINGS
# ------------------------------------------------------------------------------

AJAX_LOOKUP_CHANNELS = {

'cities_light_country': ('cities_light.lookups', 'CountryLookup'),
'cities_light_city': ('cities_light.lookups', 'CityLookup'),

}
'''

# CONTROLCENTER SETTINGS
# ------------------------------------------------------------------------------

CONTROLCENTER_DASHBOARDS = (
    'gglobal.crm.admin.MyDashboard',
)

# CONTROLCENTER SETTINGS 
# ------------------------------------------------------------------------------

AVATAR_GRAVATAR_FORCEDEFAULT = True
AVATAR_GRAVATAR_DEFAULT = 'identicon'



# DJANGO_MONEY_RATES SETTINGS 
# ------------------------------------------------------------------------------

DJANGO_MONEY_RATES = {
    'DEFAULT_BACKEND': 'djmoney_rates.backends.OpenExchangeBackend',
    'OPENEXCHANGE_URL': 'http://openexchangerates.org/api/latest.json',
    'OPENEXCHANGE_APP_ID': 'd7f21191cfa74010996bfc70c673e36f',
    'OPENEXCHANGE_BASE_CURRENCY': 'USD',
}

'''
# DOGSLOW SETTINGS
# ------------------------------------------------------------------------------


# Watchdog is enabled by default, to temporarily disable, set to False:
DOGSLOW = True

# By default, Watchdog will create log files with the backtraces.
# You can also set the location of where it stores them:
DOGSLOW_LOG_TO_FILE = True
DOGSLOW_OUTPUT = '/tmp'

# Log requests taking longer than 25 seconds:
DOGSLOW_TIMER = 25

# When both specified, emails backtraces:
DOGSLOW_EMAIL_TO = 'errors@atlassian.com'
DOGSLOW_EMAIL_FROM = 'no-reply@atlassian.com'

# Also log to this logger (defaults to none):
DOGSLOW_LOGGER = 'syslog_logger'
DOGSLOW_LOG_LEVEL = 'WARNING'

# Tuple of url pattern names that should not be monitored:
# (defaults to none -- everything monitored)
# Note: this option is not compatible with Django < 1.3
DOGSLOW_IGNORE_URLS = ('some_view', 'other_view')

# Print (potentially huge!) local stack variables (off by default, use
# True for more detailed, but less manageable reports)
DOGSLOW_STACK_VARS = True
'''