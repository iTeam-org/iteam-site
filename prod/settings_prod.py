#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))

################################
# Basic and misc
################################

DEBUG = False
TEMPLATE_DEBUG = False
SERVE = False

ALLOWED_HOSTS = ['localhost']

# Make this unique, and don't share it with anybody.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z3rte+c4hikqi-csxbs2&j#+5%nwwbe=ki0j957a^i1%k-hs^^'

################################
# Static and media
################################

STATIC_ROOT = '/opt/iteam-env/static'
STATIC_URL = '/static/'

MEDIA_ROOT = '/opt/iteam-env/media'
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    ('stylesheets', os.path.join(SITE_ROOT, 'assets', 'stylesheets')),
    ('javascripts', os.path.join(SITE_ROOT, 'assets', 'javascripts')),
    ('images', os.path.join(SITE_ROOT, 'assets', 'images')),
)

################################
# Database
################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}

################################
# Email and errors report
################################

EMAIL_HOST = 'mail.mailoo.org'
EMAIL_HOST_USER = '**********'
EMAIL_HOST_PASSWORD = '*********'
EMAIL_PORT = 25

# Email address that error messages come from.
SERVER_EMAIL = 'siteweb@iteam.org'
# Default email address to use for various automated correspondence from the site managers.
DEFAULT_FROM_EMAIL = 'siteweb@iteam.org'

# Subject-line prefix for email messages send with django.core.mail.mail_admins or ...mail_managers.
# Make sure to include the trailing space.
EMAIL_SUBJECT_PREFIX = '[Django] '

# People who get code error notifications.
ADMINS = (('John Doe', 'johndoe@gmail.com'),)
# Not-necessarily-technical managers of the site. They get broken link notifications and other various emails.
MANAGERS = ADMINS

# Whether to send broken-link emails. Deprecated, must be removed in 1.8.
SEND_BROKEN_LINK_EMAILS = False

"""
IGNORABLE_404_URLS = (
        re.compile(r'^/apple-touch-icon.*\.png$'),
        re.compile(r'^/favicon.ico$'),
        re.compile(r'^/robots.txt$'),
    )
"""
