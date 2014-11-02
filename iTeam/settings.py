#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Adrien Chardon
# @Date:   2014-09-02 12:01:06
# @Last Modified by:   Adrien Chardon
# @Last Modified time: 2014-11-02 17:17:31

# This file is part of iTeam.org.
# Copyright (C) 2014 Adrien Chardon (Nodraak).
#
# iTeam.org is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# iTeam.org is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with iTeam.org. If not, see <http://www.gnu.org/licenses/>.

"""
Django settings for iTeam project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

#############################
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
#############################

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import datetime

################################
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
################################

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'fr-FR'  # default : 'en-us'

TIME_ZONE = 'Europe/Paris'  # default : 'UTC'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True


##################################
# Files location
##################################
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(SITE_ROOT, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
# STATIC_ROOT = os.path.join(SITE_ROOT, 'static') # dont uncomment, the css are not found anymore

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(SITE_ROOT, 'assets'),
)

# Absolute path to template directory (/Library/Python/2.7/site-packages/django)
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)


###############################
# Dev options for debug
###############################

# Make this unique, and don't share it with anybody.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z3rte+c4hikqi-csxbs2&j#+5%nwwbe=ki0j957a^i1%k-hs^^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

# Should Django serve the static and media files ? This should not be set to
# True in a production environment
SERVE = True

ALLOWED_HOSTS = ['localhost']


##################################
# Stuff divers
##################################

# Application definition

INSTALLED_APPS = (
    'iTeam.pages',
    'iTeam.member',
    'iTeam.publications',
    'iTeam.medias',
    'iTeam.events',
    'iTeam.stats',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'email_obfuscator',
    'south',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'iTeam.middleware.Log_middleware',
)

ROOT_URLCONF = 'iTeam.urls'

WSGI_APPLICATION = 'iTeam.wsgi.application'

TEMPLATE_CONTEXT_PROCESSORS = (
    # Default context processors
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',

    # Custom context processors
    'iTeam.context_processors.git_version',
)


############################################
# Database + Cache
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
############################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


##########################################
# iTeam settings
##########################################

NB_PUBLICATIONS_PER_PAGE = 10
NB_EVENTS_PER_PAGE = 10
NB_MEMBERS_PER_PAGE = 8*10

SIZE_MAX_IMG = 5*1024*1024      # 5 Mo
SIZE_MAX_FILE = 50*1024*1024    # 50 Mo
SIZE_MAX_TITLE = 100

PUBLICATIONS_MODEL_TYPES = (
    ('N', u'News'),
    ('T', u'Tutoriel'),
    ('P', u'Publication')  # default
)

PUBLICATIONS_TYPES = [item for (item, _) in PUBLICATIONS_MODEL_TYPES]

MODEL_IS_DRAFT = (
    ('1', u'Brouillon'),
    ('0', u'Publier immédiatement'),
)

EVENTS_MODEL_TYPES = (
    ('F', u'Formation'),
    ('C', u'Conférence'),
    ('B', u'Bar'),
    ('J', u'Journée portes ouvertes'),
    ('A', u'AG'),
    ('O', u'Autre'),  # other
)

# month_str : january = 1, february = 2, ...
MONTH_STR = [
    '',
    'Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin',
    'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'
]
# month_str : Monday = 0, Tuesday = 1, ...
DAYS_STR = [
    'Lundi', 'Mardi', 'Mecredi', 'Jeudi', 'Vendredi', 'Samedi', 'Dimanche'
]

START_HOUR_UTC = 4
END_HOUR_UTC = 21

LOGIN_URL = '/membres/connexion/'

FORGOT_PASSWORD_TOKEN_EXPIRES = datetime.timedelta(hours=2)

# python social auth
"""
SOCIAL_AUTH_LOGIN_URL = LOGIN_URL

SOCIAL_AUTH_FACEBOOK_KEY = '530267980453281'
SOCIAL_AUTH_FACEBOOK_SECRET = 'bf2b79d49d208386a125c18474c92f6b'

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email', 'publish_actions']

#SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {'locale': 'ru_RU'}

SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'http://localhost:8000/login_success/'
SOCIAL_AUTH_LOGIN_ERROR_URL = '/login_fail/'
SOCIAL_AUTH_LOGIN_URL = '/login/'

SOCIAL_AUTH_USER_MODEL = 'auth.User'

SOCIAL_AUTH_SESSION_EXPIRATION = True

SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']
"""

#############################################
#
# LOGGING
#
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
#
# Levels :
# DEBUG: Low level system information for debugging purposes
# INFO: General system information
# WARNING: Information describing a minor problem that has occurred.
# ERROR: Information describing a major problem that has occurred.
# CRITICAL: Information describing a critical problem that has occurred.
##############################################

"""
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'formatters': {
        'default': {
            'format': '\tDefault : %(levelname)s %(asctime)s %(message)s'
        },
        'request': {
            'format': '\tRequest : %(levelname)s %(status_code)d %(message)s'
        },
        'backends_simple': {
            'format': '\tBackends : %(levelname)s %(asctime)s %(duration)f'
        },
        'backends_verbose': {
            'format': '\tBackends : %(levelname)s %(asctime)s %(duration)f %(sql)s'
        },
    },

    'handlers': {
        'default':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'request':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'request'
        },
        'backends':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'backends_verbose'
        },
        #'db':{
        #    'level': 'INFO',
        #    'class': 'iTeam.utils.MyDbLogHandler',
        #    'formatter': 'verbose'
        #}
    },

    'loggers': {
        'django': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['backends'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
"""

######################################
# Production settings
#
# Load the production settings from the settings_prod.py file. This will
# override some settings from this file as needed, like the SECRET_KEY and
# other production stuff.
#######################################

try:
    from settings_prod import *
except ImportError:
    print 'No settings_prod.py found, skipping ...'
