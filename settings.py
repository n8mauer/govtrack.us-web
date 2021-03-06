# -*- coding: utf-8 -*-
import os
import os.path
import sys
import re

ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(ROOT, 'lib'))

DEBUG = ("DEBUG" in os.environ)
TEMPLATE_DEBUG = DEBUG
INTERNAL_IPS = ('127.0.0.1',)

ADMINS = (
    ('Joshua Tauberer', 'tauberer@govtrack.us'),
)

MANAGERS = ADMINS

if DEBUG and "SSH_CONNECTION" in os.environ:
	# When launched from an SSH session, add the remote host to
	# the list of INTERNAL_IPSs so that he can see the SQL.
	# debugging output.
	INTERNAL_IPS = ('127.0.0.1', os.environ["SSH_CONNECTION"].split(" ")[0])
	if sys.argv == ['./manage.py', 'runserver']: print "Internal IPs:", repr(INTERNAL_IPS)
                                        
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

STATIC_URL = '/static/'

# django-regitration-pv
APP_NICE_SHORT_NAME = "GovTrack" # a short name for your site
SITE_ROOT_URL = "https://www.govtrack.us"
LOGIN_REDIRECT_URL = "/accounts/profile"
SERVER_EMAIL = "GovTrack.us <noreply@GovTrack.us>" # From: address on verification emails
REGISTRATION_ASK_USERNAME = False

SESSION_COOKIE_AGE = 6*604800 # seconds in six weeks
SESSION_COOKIE_SECURE = not DEBUG # send session cookies over SSL only
CSRF_COOKIE_SECURE = not DEBUG # similarly
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer' # needed by openid login

EMAIL_HOST = 'localhost'
EMAIL_PORT = 587
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)
if not DEBUG:
    TEMPLATE_LOADERS = (
      ('django.template.loaders.cached.Loader', TEMPLATE_LOADERS),
      )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'twostream.middleware.CacheLogic',
    'website.middleware.GovTrackMiddleware',
)

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(ROOT, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    # 3rd party libraries
    'common',
    'django_extensions',
    #'south',
    'debug_toolbar',
    
    'haystack',
    'tastypie',
    'django_wysiwyg',
    'django_twilio',
    
    # project modules
    'twostream',
    'person',
    'committee',
    'website',
    'vote',
    'parser',
    'events',
    'smartsearch',
    'bill',
    'states',
    'poll_and_call',
    'predictionmarket',

    # for django-registration-pv
    'emailverification',
    'registration',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'events.middleware.template_context_processor',
    'website.middleware.template_context_processor',
)

TEST_DATABASE_CHARSET = 'utf8'

DATETIME_FORMAT = 'M d, Y P'
DATE_FORMAT = 'M d, Y'

SEND_BROKEN_LINK_EMAILS = False
IGNORABLE_404_ENDS = ('spinner.gif', 'billtext/images/quote.png')
IGNORABLE_404_STARTS = ('/phpmyadmin/',)
import re
IGNORABLE_404_URLS = (
	re.compile(r'^/phpmyadmin/'),
	re.compile(r'spinner\.gif'),
	re.compile(r'billtext/images/quote.png$'),
	)

CURRENT_CONGRESS = 113

EMAIL_UPDATES_FROMADDR = "GovTrack.us Email Updates <noreply@GovTrack.us>"
EMAIL_UPDATES_RETURN_PATH = "bounces+uid=%d@GovTrack.us"
BOUNCES_UID_REGEX = re.compile(r"<?bounces\+uid=(\d+)@GovTrack\.us>?", re.I)

PREDICTIONMARKET_SEED_MONEY = 1000
PREDICTIONMARKET_BANK_UID = 136196

#if DEBUG: # sometimes we debug in a live environment
#	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

try:
    from settings_local import *
except ImportError:
    pass

if not SECRET_KEY:
    raise Exception('You must provide SECRET_KEY value in settings_local.py')

# Since we rely on external APIs in a few places, make sure
# that downed APIs elsewhere don't hold us too long. Not
# sure this has any useful effect.
import socket
socket.setdefaulttimeout(10.0)

