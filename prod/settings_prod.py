#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
SITE_ROOT = os.path.realpath(os.path.dirname(os.path.dirname(__file__)))


DEBUG = False
TEMPLATE_DEBUG = False
SERVE = False


ALLOWED_HOSTS = ['.famillechardon.fr', '192.168.0.100', 'localhost']
# since every request pass by nginx then gunicorn, and gunicorn proxy all via
# localhost, should we only have localhost ?

# Make this unique, and don't share it with anybody.
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z3rte+c4hikqi-csxbs2&j#+5%nwwbe=ki0j957a^i1%k-hs^^'


ADMINS = (('Adrien Chardon', 'johndoe@gmail.com'),)
SERVER_EMAIL = 'contact_iteam@famillechardon.fr'
EMAIL_HOST = 'mail.mailoo.org'
EMAIL_HOST_USER = '**********'
EMAIL_HOST_PASSWORD = '*********'
EMAIL_PORT = 25


STATIC_ROOT = os.path.join(SITE_ROOT, '..', 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(SITE_ROOT, '..', 'media')
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    ('stylesheets', os.path.join(SITE_ROOT, 'assets', 'stylesheets')),
    ('javascripts', os.path.join(SITE_ROOT, 'assets', 'javascripts')),
    ('images', os.path.join(SITE_ROOT, 'assets', 'images')),
)

